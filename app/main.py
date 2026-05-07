from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Accounting SaaS Backend Running"}