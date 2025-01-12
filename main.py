import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.endpoints.alert_message import router


load_dotenv()

app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
