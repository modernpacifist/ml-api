import fastapi

from models import InputModel


app = fastapi.FastAPI()


@app.get("/")
async def read_root(input: InputModel):
    return {"hello": "world"}


if __name__ == "__main__":
    app.run()
