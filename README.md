# py_fapi_sandbox

# license: MIT

# Packages:
 * sqlalchemy
 * fastapi

# featrues:
 * simple account for sign up / in

# Information:
  Sandbox testing web http server for fast request?

# sqlalchemy:
  Note there two methods or more depend where the docs are. One the old and other is the new api.

# run cmd:
```
uvicorn --reload --app-dir='src' main:app
```

# uvicorn
```
uvicorn main:app --reload
```
Run current dir but does not go to src.

```
pipenv run pip3 freeze > requirements.txt
```
Export package names and versions


# Refs:
 * https://stackoverflow.com/questions/73630653/redirect-to-login-page-if-user-not-logged-in-using-fastapi-login-package
 * https://samedwardes.com/2022/04/14/fastapi-webapp-with-auth/
 * https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
 * https://github.com/tiangolo/fastapi





















