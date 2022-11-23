from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse("index.html")

app.mount("/", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    print('Please run with: "uvicorn main:app"')