import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx

@asynccontextmanager
async def lifespan(app):
    yield

app = FastAPI(title="NEXUS AI Cloud", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ChatMessage(BaseModel):
    role: str
    content: str = Field(min_length=1, max_length=8000)

class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1, max_length=30)

class PlanRequest(BaseModel):
    goal: str = Field(min_length=1, max_length=4000)

@app.get("/")
async def root():
    return {"name":"NEXUS AI","status":"online","message":"Backend cloud activo."}

@app.get("/health")
async def health():
    configured = bool(os.getenv("NEXUS_API_BASE") and os.getenv("NEXUS_API_KEY") and os.getenv("NEXUS_MODEL"))
    return {"ok":True,"name":"NEXUS AI","version":"1.0.0","provider_configured":configured}

@app.get("/api/status")
async def status():
    return {"online":True,"chat_provider_configured":bool(os.getenv("NEXUS_API_BASE") and os.getenv("NEXUS_API_KEY") and os.getenv("NEXUS_MODEL")),"execution_tools_enabled":False}

@app.get("/api/agents")
async def agents():
    return {"agents":[{"id":"architect","name":"Arquitecto"},{"id":"researcher","name":"Investigador"},{"id":"developer","name":"Programador"},{"id":"designer","name":"Diseñador"},{"id":"reviewer","name":"Revisor"},{"id":"tester","name":"Tester"}]}

@app.post("/api/chat")
async def chat(body: ChatRequest):
    base=os.getenv("NEXUS_API_BASE","").strip().rstrip("/")
    key=os.getenv("NEXUS_API_KEY","").strip()
    model=os.getenv("NEXUS_MODEL","").strip()
    if not (base and key and model):
        return {"mode":"setup_required","reply":"NEXUS AI está conectado al servidor online, pero falta configurar el proveedor de IA en la nube. La conexión funciona; las respuestas reales se habilitan al agregar una clave API compatible en Render."}
    messages=[m.model_dump() for m in body.messages]
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(60,connect=10)) as client:
            response=await client.post(base+"/chat/completions",headers={"Authorization":"Bearer "+key},json={"model":model,"messages":messages,"temperature":0.4})
            response.raise_for_status()
        data=response.json()
        reply=data["choices"][0]["message"]["content"]
        if isinstance(reply,list):
            reply="\n".join(str(x.get("text","")) for x in reply if isinstance(x,dict))
        if not isinstance(reply,str) or not reply.strip():
            raise ValueError("empty response")
        return {"mode":"connected","reply":reply.strip()}
    except httpx.TimeoutException as exc:
        raise HTTPException(504,"El proveedor de IA tardó demasiado.") from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(502,f"El proveedor devolvió HTTP {exc.response.status_code}.") from exc
    except (httpx.HTTPError,KeyError,IndexError,TypeError,ValueError) as exc:
        raise HTTPException(502,"No se pudo procesar la respuesta del proveedor.") from exc

@app.post("/api/plan")
async def plan(body: PlanRequest):
    goal=body.goal.strip()
    if not goal:
        raise HTTPException(422,"Escribí un objetivo.")
    return {"mode":"template","goal":goal,"tasks":[
      {"id":"T1","agent":"architect","title":"Definir requisitos y arquitectura","status":"pending"},
      {"id":"T2","agent":"researcher","title":"Investigar alternativas y dependencias","status":"pending"},
      {"id":"T3","agent":"developer","title":"Implementar la solución","status":"pending"},
      {"id":"T4","agent":"tester","title":"Probar y corregir","status":"pending"}],
      "note":"Plan inicial. Las tareas no se ejecutan automáticamente."}
