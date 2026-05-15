from typing import Dict

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest

from app.services.chain import build_chain

from app.services.logger import logger, request_id_var , get_extra
import uuid

app = FastAPI()
security = HTTPBasic()

# Dummy user database
users_db: Dict[str, Dict[str, str]] = {
    "Tony": {"password": "password123", "role": "engineering"},
    "Bruce": {"password": "securepass", "role": "marketing"},
    "Sam": {"password": "financepass", "role": "finance"},
    "Peter": {"password": "pete123", "role": "engineering"},
    "Sid": {"password": "sidpass123", "role": "marketing"},
    "Natasha": {"password": "hrpass123", "role": "hr"}
}


# Authentication dependency
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    user = users_db.get(username)
    if not user or user["password"] != password:
        logger.warning(msg="Authentication Failed! Password mismatch",extra= get_extra(user_name=credentials.username))
        raise HTTPException(status_code=401, detail="Invalid credentials")  
    logger.info("Authentication Successfull",extra=get_extra(user_name=credentials.username, role=user["role"]))
    return {"username": username, "role": user["role"]}


# Login endpoint
@app.get("/login")
def login(user=Depends(authenticate)):
    return {"message": f"Welcome {user['username']}!", "role": user["role"]}


# Protected test endpoint
@app.get("/test")
def test(user=Depends(authenticate)):
    return {"message": f"Hello {user['username']}! You can now chat.", "role": user["role"]}


# Protected chat endpoint
@app.post("/chat")
async def query(request: ChatRequest,user=Depends(authenticate)) :
    session_key=  f"{user['username']}:{request.session_id}"
    user_role= user['role']
    message= request.message
    #ContextVar
    request_id= str(uuid.uuid4())
    request_id_var.set(request_id)
    logger.info("chat_request_started", extra=get_extra(session_id=session_key, role=user_role, user_name= user['username'] ))
    async def generate():
        async for chunk in build_chain(user_role).astream(
        {'question' :message},
        config={"configurable": {"session_id": session_key}}):
            yield chunk
    return StreamingResponse(generate(), media_type="text/plain")