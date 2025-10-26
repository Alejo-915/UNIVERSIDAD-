from fastapi import FastAPI
app = FastAPI()
app.get("/")
app.get("/item")
def root():
    return {"message": "Hello World"}
