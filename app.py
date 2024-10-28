import uvicorn
from fastapi import FastAPI


def main():
    app = FastAPI()
    uvicorn.run('app:app', reload=True)


if __name__ == '__main__':
    main()
