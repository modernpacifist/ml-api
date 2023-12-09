import fastapi


app = fastapi.FastAPI()


@app.get("/")
async def read_root():
    return {"hello": "world"}


def main():
    app.run()


if __name__ == "__main__":
    main()
