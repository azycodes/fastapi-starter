"""
Title: Learning notes for FastAPIs
Author: AzyCodes
install: pip install "fastapi[all]"
"""
from typing import List
from fastapi import FastAPI, Path, Query, Body, Form, File, UploadFile, Header, Request
from enum import Enum
from pydantic import BaseModel

app = FastAPI()


class UserType(str, Enum):
    NORMAL = "normal"
    ADMIN = "admin"


# normal view
@app.get("/")
async def home():
    return {"msg": "Welcome to FastAPI"}


# path params
@app.get("/users/{type}/{id}")
async def users(id: int = Path(..., ge=5), type: UserType = Path(...)):
    return {"user_id": id, "type": type}


# query params
@app.get("/posts/")
async def posts(page: int = None, limit: int = Query(1, ge=0), filter: str = None):
    return {"msg": f"page no: {page}, limit: {limit}, filter: {filter}"}


# adavnce Path
@app.get("/license/{licence_id}")
async def get_license(licence_id: str = Path(..., regex=r"^\w{2}-\d{3}-\w{2}$")):
    return {"msg": f"Licence ID: {licence_id}"}


# post request with body param
@app.post("/user/")
async def create_user(name: str = Body(...), age: int = Body(...)):
    return {"name": name, age: age}


# Using pydantic models


class User(BaseModel):
    fname: str
    lname: str
    age: int


@app.post("/user/add")
async def add_user(user: User):
    return user


# multiple objects


class Company(BaseModel):
    name: str
    address: str


@app.post("/user/company")
async def user_company(user: User, company: Company):
    return {"user": user, "company": company}


# singlular body


class Alert(BaseModel):
    id: int
    title: str
    desc: str


@app.post("/alert/add")
async def add_alert(alert: Alert, severity=Body(...)):
    data = {
        "id": alert.id,
        "title": alert.title,
        "severity": severity,
        "desc": alert.desc,
    }
    return data


# Accepting Form Data


@app.post("/user/plus")
async def plus_user(name: str = Form(...), age: int = Form(...)):
    return {"name": name, "age": age}


#  File upload: in memory -> inefficient
@app.post("/file/upload")
async def file_upload(file: bytes = File(...)):
    return {"file_upload": len(file)}


# File upload: in memory for some limit later saved in temp -> efficient
@app.post("/file/ups")
async def file_ups(file: UploadFile = File(...)):
    return {"file_name": file.filename, "content_type": file.content_type}


# File upload, multiple files
@app.post("/files/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    return [
        {"file_name": file.filename, "content_type": file.content_type}
        for file in files
    ]


# Headers
@app.get("/headers")
async def get_headers(name: str = Header(...)):
    return {"headers": name}


# Request obj
@app.get("/request")
async def req(req: Request):
    return {"path": req.url.path}
