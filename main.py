from .server import app
import uvicorn

def main():
    uvicorn.run(app,host='127.0.0.1',port=3000)
main()