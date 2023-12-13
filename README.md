### Requirements
[Poetry](https://python-poetry.org/docs/) package >= 1.4

### Run
### Via poetry
```
$ cd ./src
$ poetry install
$ poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
### Via Docker
```
$ docker-compose up
```
