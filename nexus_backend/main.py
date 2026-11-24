import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx

app = FastAPI(title="NEXUS AI Cloud", version="1.0.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

projects=[]
memories=[]
next_project_id=1
next_memory_id=1

class ChatMessage(BaseModel):
    role: str
    content: str = Field(min_length=1, max_length=8000)
class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1, max_length=30)
class PlanRequest(BaseModel):
    goal: str = Field(min_length=1, max_length=4000)
class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=2000)
class MemoryCreate(BaseModel):
    content: str = Field(min_length=1, max_length=4000)
    project_id: int | None = None
    tags: list[str] = Field(default_factory=list, max_length=10)

@app.get("/")
async def root():
    return {"name":"NEXUS AI","status":"online","message":"Backend cloud activo."}
@app.get("/health")
async def health():
    return {"ok":True,"name":"NEXUS AI","version":"1.0.1","provider_configured":bool(os.getenv("NEXUS_API_BASE") and os.getenv("NEXUS_API_KEY") and os.getenv("NEXUS_MODEL"))}
@app.get("/api/status")
async def status():
    return {"online":True,"chat_provider_configured":bool(os.getenv("NEXUS_API_BASE") and os.getenv("NEXUS_API_KEY") and os.getenv("NEXUS_MODEL")),"execution_tools_enabled":False,"persistent_projects":False,"persistent_memory":False}
@app.get("/api/agents")
async def agents():
    return {"agents":[{"id":"architect","name":"Arquitecto"},{"id":"researcher","name":"Investigador"},{"id":"developer","name":"Programador"},{"id":"designer","name":"Diseñador"},{"id":"reviewer","name":"Revisor"},{"id":"tester","name":"Tester"}]}
@app.post("/api/chat")
async def chat(body: ChatRequest):
    base=os.getenv("NEXUS_API_BASE","").strip().rstrip("/")
    key=os.getenv("NEXUS_API_KEY","").strip()
    model=os.getenv("NEXUS_MODEL","").strip()
    if not (base and key and model):
        return {"mode":"setup_required","reply":"NEXUS AI está conectado al servidor online, pero falta configurar el proveedor de IA en la nube. La conexión funciona; las respuestas reales se habilitan al agregar un proveedor compatible en Render."}
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(60,connect=10)) as client:
            response=await client.post(base+"/chat/completions",headers={"Authorization":"Bearer "+key},json={"model":model,"messages":[m.model_dump() for m in body.messages],"temperature":0.4})
            response.raise_for_status()
        reply=response.json()["choices"][0]["message"]["content"]
        if isinstance(reply,list): reply="\n".join(str(x.get("text","")) for x in reply if isinstance(x,dict))
        if not isinstance(reply,str) or not reply.strip(): raise ValueError("empty")
        return {"mode":"connected","reply":reply.strip()}
    except httpx.TimeoutException as exc: raise HTTPException(504,"El proveedor de IA tardó demasiado.") from exc
    except httpx.HTTPStatusError as exc: raise HTTPException(502,f"El proveedor devolvió HTTP {exc.response.status_code}.") from exc
    except (httpx.HTTPError,KeyError,IndexError,TypeError,ValueError) as exc: raise HTTPException(502,"No se pudo procesar la respuesta del proveedor.") from exc
@app.post("/api/plan")
async def plan(body: PlanRequest):
    goal=body.goal.strip()
    if not goal: raise HTTPException(422,"Escribí un objetivo.")
    return {"mode":"template","goal":goal,"tasks":[{"id":"T1","agent":"architect","title":"Definir requisitos y arquitectura","status":"pending"},{"id":"T2","agent":"researcher","title":"Investigar alternativas y dependencias","status":"pending"},{"id":"T3","agent":"developer","title":"Implementar la solución","status":"pending"},{"id":"T4","agent":"tester","title":"Probar y corregir","status":"pending"}],"note":"Plan inicial. Las tareas no se ejecutan automáticamente."}
@app.get("/api/projects")
async def get_projects():
    return {"projects":projects}
@app.post("/api/projects",status_code=201)
async def add_project(body: ProjectCreate):
    global next_project_id
    item={"id":next_project_id,"name":body.name.strip(),"description":body.description.strip(),"status":"active"}
    if not item["name"]: raise HTTPException(422,"Nombre vacío.")
    next_project_id+=1; projects.append(item)
    return {"project":item}
@app.delete("/api/projects/{project_id}")
async def delete_project(project_id:int):
    for i,item in enumerate(projects):
        if item["id"]==project_id:
            projects.pop(i); return {"deleted":True,"project_id":project_id}
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
    next_memory_id+=1; memories.insert(0,item)
    return {"memory":item}
