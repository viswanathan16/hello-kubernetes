from fastapi import FastAPI
import socket
import os

app = FastAPI()

@app.get("/info")
def get_info():
    return {
        "message": "Hello from FastAPI!",
        "pod_name": socket.gethostname(),
        "node_name": os.getenv("NODE_NAME", "Unknown"),
        "namespace": os.getenv("POD_NAMESPACE", "default"),
        "image_version": os.getenv("IMAGE_VERSION", "1.0.0")
    }

@app.get("/")
def root():
    return { 
             "message": "Welcome to the FastAPI microservice!"
             "info": f"Hi! This is {pod_name} pod responding to your request."
            }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

