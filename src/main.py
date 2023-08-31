# https://fastapi.tiangolo.com/advanced/templates/
# https://www.uvicorn.org/
#python
import asyncio
import datetime
#server
import uvicorn
#fastapi
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

#database
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import select
#================================================
# TABLE
#================================================
class Base(DeclarativeBase):
  pass
# https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
class User(Base):
  __tablename__ = "user_account"

  id: Mapped[int] = mapped_column(primary_key=True)
  #name: Mapped[str] = mapped_column(String(30))
  name: Mapped[Optional[str]]
  fullname: Mapped[Optional[str]]

  alias: Mapped[str] = mapped_column(String(30))
  passphrase: Mapped[str] = mapped_column(String(64))

  #created_at: Mapped[TIMESTAMP] = mapped_column(
  created_at: Mapped[TIMESTAMP] = mapped_column(
    #DateTime(timezone=True),
    TIMESTAMP,
    #server_default=func.now()
    #server_default=func.current_timestamp()
    default=datetime.datetime.utcnow
  )
  updated_at: Mapped[datetime.datetime] = mapped_column(
    DateTime(timezone=True),
    default=datetime.datetime.utcnow,
    onupdate=datetime.datetime.utcnow
  )

  def __repr__(self) -> str:
    return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r}, alias={self.alias})"
  
#init set up database
engine = create_engine("sqlite:///database.sqlite", echo=True)
#create table
Base.metadata.create_all(engine)

#================================================
# APP
#================================================
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

#================================================
# INDEX
#================================================
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
  #print("hello world")
  #return {"Hello": "World"}
  token = request.cookies.get('token')
  id="None"
  if token:
    print("FOUND TOKEN...")
    return templates.TemplateResponse("home.html", {"request": request, "id": id})  
  
  #if not login return default
  return templates.TemplateResponse("index.html", {"request": request, "id": id})

#================================================
# SIGN IN
#================================================
@app.get("/signin", response_class=HTMLResponse)
def read_login(request: Request):
  #return {"Hello": "World"}
  id="None"
  return templates.TemplateResponse("signin.html", {"request": request, "id": id})

class SignIn_User(BaseModel):
  alias:str
  passphrase:str

@app.post("/api/auth/signin")
def auth_login(user: SignIn_User):
  print("LOGIN AUTH:",user)
  content = {"api":"FAIL"}
  response = None
  try:
    with Session(engine) as session:
      result = session.execute(select(User).where(User.alias == user.alias)).scalar()# one row else return None
      print("RESULT: ", result)
      content = {"api":"FAIL"}
      if result:
        print("USER:", result.id)
        if result.passphrase == user.passphrase:
          content = {"api":"PASS"}
          response = JSONResponse(content=content)
          response.set_cookie(key="token", value="fake-cookie-session-value")
        else:
          content = {"api":"DENIED"}
          response = JSONResponse(content=content)
      else:
        content = {"api":"NONEXIST"}
        response = JSONResponse(content=content)
      return response
  except :
    print("USER SIGN UP ERROR!")
    pass
  response = JSONResponse(content=content)
  #response.set_cookie(key="token", value="fake-cookie-session-value")
  return response
#================================================
# SIGN UP
#================================================
@app.get("/signup", response_class=HTMLResponse)
def read_login(request: Request):
  #return {"Hello": "World"}
  id="Guest"
  return templates.TemplateResponse("signup.html", {"request": request, "id": id})

class SignUp_User(BaseModel):
  alias:str
  passphrase:str
  #email:str

@app.post("/api/auth/signup")
async def auth_signup(user: SignUp_User):
  print(user)
  print("alias: ",user.alias)
  #return user
  try:
    with Session(engine) as session:
      #stmt = select(User).where(User.alias == user.alias)
      #current_user = session.scalars(stmt).one()
      #result = session.query(User).where(User.alias == user.alias).all()# pass

      #stmt = select(User).where(User.alias == user.alias) #ok
      #result = session.execute(stmt)

      #result = session.execute(select(User).where(User.alias == user.alias))
      #result = session.execute(select(User).where(User.alias == user.alias)).first()# row else return None
      result = session.execute(select(User).where(User.alias == user.alias)).scalar()# if nothing return None

      print("RESULT: ", result)
      if result:
        print("FOUND")
        print("USER:", result)
        print("USER:", result.id)
        return {"api":"EXIST"}
      else:
        newUser = User(
          alias = user.alias,
          passphrase = user.passphrase
        )
        session.add_all([newUser])
        session.commit()
        return {"api":"PASS"}
  except :
    print("USER SIGN UP ERROR!")
    pass

  return {"api":"FAIL"}
  
#================================================
# SIGN OUT
#================================================
@app.get("/signout", response_class=HTMLResponse)
def read_signout(request: Request):
  #return {"Hello": "World"}
  id="Guest"
  return templates.TemplateResponse("signout.html", {"request": request, "id": id})

@app.post("/api/auth/signout")
def auth_signout(request: Request):
  token = request.cookies.get('token')
  content = {"api": "ERROR"}
  if token:
    content = {"api": "LOGOUT"}
    response = JSONResponse(content=content)
    response.set_cookie(key="token",expires=0)
    return response
  return content

#================================================
# ADMIN
#================================================
@app.get("/admin", response_class=HTMLResponse)
def read_admin(request: Request):
  #return {"Hello": "World"}
  id="Guest"
  return templates.TemplateResponse("admin.html", {"request": request, "id": id})






#================================================
# Test
#================================================

# https://fastapi.tiangolo.com/advanced/response-cookies/
#@app.post("/cookie-and-object/")
@app.get("/cookie1")
def create_cookie(response: Response):
  content = {"message": "Come to the dark side, we have cookies1"}
  #response = JSONResponse(content=content)
  response.set_cookie(key="fakesession", value="fake-cookie-session-value1")
  return content

@app.get("/cookie2")
def create_cookie2():
  content = {"message": "Come to the dark side, we have cookies2"}
  response = JSONResponse(content=content)
  response.set_cookie(key="fakesession", value="fake-cookie-session-value2")
  return response

#for some reason reload does not work on window or incorrect config
async def main():
  #print("hello")
  config = uvicorn.Config(
    "main:app", 
    port=5000, 
    log_level="info",
    reload = True,
    reload_dirs=['src'],
    reload_includes=['*.py']
  )
  #config.reload = True
  #config.reload_dirs = ['.']
  #config.reload_includes
  server = uvicorn.Server(config)
  #server.run()
  await server.serve()

# main if exist
if __name__ == '__main__':
  #main()
  asyncio.run(main())