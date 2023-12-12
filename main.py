import fastapi

from models import 


app = fastapi.FastAPI()


@app.get("/")
async def read_root():
    return {"hello": "world"}


if __name__ == "__main__":
    app.run()
