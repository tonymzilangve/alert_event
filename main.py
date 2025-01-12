import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
