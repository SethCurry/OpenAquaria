from fastapi import FastAPI

app = FastAPI()


class API:
    def __init__(self, app: FastAPI):
        self.app = app
