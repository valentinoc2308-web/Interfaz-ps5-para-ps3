"""NEXUS AI multi-provider gateway. Secrets stay server-side."""
import json, os, time, hmac
from collections import defaultdict, deque
from typing import Literal
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

app=FastAPI(title="NEXUS AI Multi-Model Cloud",version="0.10.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

# API access gate and basic per-IP request throttling.
_rate_buckets = defaultdict(deque)
@app.middleware("http")
async def protect_api(request: Request, call_next):
    if request.url.path.startswith("/api/"):
        expected = os.getenv("NEXUS_ACCESS_TOKEN", "").strip()
        supplied = request.headers.get("authorization", "")
        if not expected:
            return JSONResponse(status_code=503, content={"detail":"El servidor no tiene configurado NEXUS_ACCESS_TOKEN."})
        if not supplied.startswith("Bearer ") or not hmac.compare_digest(supplied[7:], expected):
            return JSONResponse(status_code=401, content={"detail":"Token de acceso inválido o faltante."})
        now = time.monotonic()
        ip = request.client.host if request.client else "unknown"
        bucket = _rate_buckets[ip]
        while bucket and now - bucket[0] > 60:
            bucket.popleft()
        if len(bucket) >= 60:
            return JSONResponse(status_code=429, content={"detail":"Límite temporal alcanzado. Probá de nuevo en un minuto."})
        bucket.append(now)
    return await call_next(request)

DIRECTORY=[
("openai","OpenAI","openai"),("anthropic","Anthropic / Claude","anthropic"),("google","Google / Gemini","gemini"),
("xai","xAI / Grok","openai"),("deepseek","DeepSeek","openai"),("mistral","Mistral AI","openai"),
("cohere","Cohere","openai"),("alibaba-qwen","Alibaba / Qwen","openai"),("moonshot","Moonshot / Kimi","openai"),
("zai","Z.ai / GLM","openai"),("baidu","Baidu / ERNIE","openai"),("bytedance","ByteDance / Doubao","openai"),
("nvidia","NVIDIA NIM","openai"),("amazon-bedrock","Amazon Bedrock","openai"),("azure","Azure AI Foundry","openai"),
("openrouter","OpenRouter","openai"),("together","Together AI","openai"),("groq","Groq","openai"),
("fireworks","Fireworks AI","openai"),("cerebras","Cerebras","openai"),("sambanova","SambaNova","openai"),
("huggingface","Hugging Face Inference","openai"),("cloudflare","Cloudflare Workers AI","openai"),("ollama","Ollama (servidor propio)","openai")]

class Msg(BaseModel):
    role: Literal["system","user","assistant"]
    content: str=Field(min_length=1,max_length=12000)
class Chat(BaseModel):
    messages: list[Msg]=Field(min_length=1,max_length=40)
    provider: str|None=Field(default=None,max_length=80)
    model: str|None=Field(default=None,max_length=160)
    @field_validator("messages")
    @classmethod
    def user_required(cls,v):
        if not any(m.role=="user" for m in v): raise ValueError("Falta mensaje del usuario.")
        return v
class Plan(BaseModel):
    goal: str=Field(min_length=1,max_length=4000)
class ProjectCreate(BaseModel):
    name: str=Field(min_length=1,max_length=100)
    description: str=Field(default="",max_length=2000)
class MemoryCreate(BaseModel):
    content: str=Field(min_length=1,max_length=4000)
    project_id: int|None=None
    tags: list[str]=Field(default_factory=list,max_length=10)

def configs():
    raw=os.getenv("NEXUS_PROVIDERS_JSON","").strip()
    if raw:
        try:
            arr=json.loads(raw)
            if not isinstance(arr,list): return []
            out=[]
            for p in arr:
                if not isinstance(p,dict): continue
                if p.get("id") and p.get("base_url") and p.get("api_key") and p.get("kind","openai") in ("openai","anthropic","gemini") and isinstance(p.get("models"),list):
                    models=[m for m in p["models"] if isinstance(m,dict) and m.get("id")]
                    if models: out.append({**p,"models":models})
            return out
        except (ValueError,TypeError): return []
    b,k,m=(os.getenv(x,"").strip() for x in ("NEXUS_API_BASE","NEXUS_API_KEY","NEXUS_MODEL"))
    return [{"id":"default","name":"Proveedor principal","kind":"openai","base_url":b,"api_key":k,"models":[{"id":m}]}] if b and k and m else []

@app.get("/")
async def root(): return {"name":"NEXUS AI","status":"online","version":"0.10.0"}
@app.get("/health")
async def health(): return {"ok":True,"name":"NEXUS AI","version":"0.9.0","provider_configured":bool(configs()),"configured_provider_count":len(configs())}
@app.get("/api/status")
async def status(): return {"online":True,"multi_provider":True,"configured_provider_count":len(configs()),"chat_provider_configured":bool(configs()),"execution_tools_enabled":False,"persistent_projects":False,"persistent_memory":False,"version":"0.9.0"}
@app.get("/api/agents")
async def agents():
    return {"agents":[{"id":"architect","name":"Arquitecto"},{"id":"researcher","name":"Investigador"},{"id":"developer","name":"Programador"},{"id":"designer","name":"Diseñador"},{"id":"reviewer","name":"Revisor"},{"id":"tester","name":"Tester"}]}

@app.get("/api/providers")
@app.get("/api/models")
async def providers():
    active=configs(); ids={p["id"] for p in active}
    return {"providers":[{"id":p["id"],"name":p.get("name",p["id"]),"kind":p.get("kind","openai"),"models":[{"id":m["id"],"name":m.get("name",m["id"])} for m in p["models"]],"configured":True} for p in active],
    "directory":[{"id":i,"name":n,"kind":k,"configured":i in ids} for i,n,k in DIRECTORY],
    "note":"El directorio son integraciones posibles; solo los proveedores configurados con credenciales y modelos están disponibles."}

async def request_json(url,headers,payload):
    async with httpx.AsyncClient(timeout=httpx.Timeout(90,connect=15)) as c:
        r=await c.post(url,headers=headers,json=payload); r.raise_for_status(); return r.json()
async def ask(p,model,messages):
    kind=p.get("kind","openai"); base=p["base_url"].rstrip("/"); key=p["api_key"]
    if kind=="anthropic":
        url=base if base.endswith("/messages") else base+"/messages"
        system="\n\n".join(m["content"] for m in messages if m["role"]=="system")
        payload={"model":model,"max_tokens":4096,"messages":[{"role":m["role"],"content":m["content"]} for m in messages if m["role"]!="system"]}
        if system: payload["system"]=system
        data=await request_json(url,{"x-api-key":key,"anthropic-version":"2023-06-01","content-type":"application/json"},payload)
        return "\n".join(x.get("text","") for x in data.get("content",[]) if x.get("type")=="text").strip()
    if kind=="gemini":
        url=base if "?" in base else f"{base}/models/{model}:generateContent?key={key}"
        system="\n\n".join(m["content"] for m in messages if m["role"]=="system")
        payload={"contents":[{"role":"model" if m["role"]=="assistant" else "user","parts":[{"text":m["content"]}]} for m in messages if m["role"]!="system"],"generationConfig":{"temperature":0.4}}
        if system: payload["systemInstruction"]={"parts":[{"text":system}]}
        data=await request_json(url,{"content-type":"application/json"},payload)
        return "\n".join(x.get("text","") for x in data.get("candidates",[{}])[0].get("content",{}).get("parts",[]) if "text" in x).strip()
    url=base if base.endswith("/chat/completions") else base+"/chat/completions"
    data=await request_json(url,{"Authorization":"Bearer "+key,"Content-Type":"application/json"},{"model":model,"messages":messages,"temperature":0.4})
    value=data.get("choices",[{}])[0].get("message",{}).get("content","")
    if isinstance(value,list): value="\n".join(x.get("text","") for x in value if isinstance(x,dict))
    return value.strip() if isinstance(value,str) else ""

@app.post("/api/chat")
async def chat(body:Chat):
    ps=configs()
    if not ps: return {"mode":"setup_required","reply":"El servidor está online, pero todavía no hay proveedores de IA configurados. Configurá NEXUS_PROVIDERS_JSON en las variables privadas de Render. Nunca guardes claves en la APK."}
    p=next((x for x in ps if body.provider and x["id"]==body.provider),None)
    if body.provider and not p: raise HTTPException(400,"Proveedor no configurado.")
    p=p or ps[0]; model=body.model or p["models"][0]["id"]
    if not any(x["id"]==model for x in p["models"]): raise HTTPException(400,"Modelo no habilitado para este proveedor.")
    try:
        answer=await ask(p,model,[m.model_dump() for m in body.messages])
        if not answer: raise ValueError("empty")
        return {"mode":"connected","provider":p["id"],"model":model,"reply":answer}
    except httpx.TimeoutException as e: raise HTTPException(504,"El proveedor tardó demasiado.") from e
    except httpx.HTTPStatusError as e: raise HTTPException(502,f"El proveedor devolvió HTTP {e.response.status_code}.") from e
    except (httpx.HTTPError,ValueError,KeyError,IndexError,TypeError) as e: raise HTTPException(502,"No se pudo procesar la respuesta del proveedor.") from e

@app.post("/api/plan")
async def plan(body:Plan):
    goal=body.goal.strip()
    if not goal: raise HTTPException(422,"Escribí un objetivo.")
    return {"mode":"template","goal":goal,"tasks":[{"id":"T1","agent":"architect","title":"Definir requisitos y arquitectura","status":"pending"},{"id":"T2","agent":"researcher","title":"Investigar alternativas y dependencias","status":"pending"},{"id":"T3","agent":"developer","title":"Implementar la solución","status":"pending"},{"id":"T4","agent":"tester","title":"Probar y corregir","status":"pending"}],"note":"Plan inicial; no se ejecuta automáticamente."}

projects=[]; memories=[]; next_project_id=1; next_memory_id=1
@app.get("/api/projects")
async def get_projects(): return {"projects":projects}
@app.post("/api/projects",status_code=201)
async def add_project(body:ProjectCreate):
    global next_project_id
    item={"id":next_project_id,"name":body.name.strip(),"description":body.description.strip(),"status":"active"}
    next_project_id+=1; projects.append(item); return {"project":item}
@app.delete("/api/projects/{project_id}")
async def delete_project(project_id:int):
    for i,p in enumerate(projects):
        if p["id"]==project_id: projects.pop(i); return {"deleted":True,"project_id":project_id}
    raise HTTPException(404,"Proyecto no encontrado.")
@app.get("/api/memory")
async def get_memory(query:str="",project_id:int|None=None,limit:int=50):
    found=[m for m in memories if (project_id is None or m["project_id"]==project_id) and query.lower() in m["content"].lower()]
    return {"memories":found[:max(1,min(limit,100))]}
@app.post("/api/memory",status_code=201)
async def add_memory(body:MemoryCreate):
    global next_memory_id
    if body.project_id is not None and not any(p["id"]==body.project_id for p in projects): raise HTTPException(404,"Proyecto no encontrado.")
    item={"id":next_memory_id,"project_id":body.project_id,"content":body.content.strip(),"tags":body.tags[:10]}
    next_memory_id+=1; memories.insert(0,item); return {"memory":item}
