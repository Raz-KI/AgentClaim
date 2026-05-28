from fastapi import FastAPI

app = FastAPI(title="Plum Claims AI")

@app.get("/health")
async def health():
    return {"status": "healthy"}