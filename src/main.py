from config.settings import HOST, PORT
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app", host=HOST, port=int(PORT))
# TODO:
# - 1 paginar los endpoints
# - 2 agregar tests
