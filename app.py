from fastapi import FastAPI
import socket
import os

app = FastAPI()

@app.get("/info")
def get_info():
    pod_name = socket.gethostname()
    node_name = os.getenv("NODE_NAME", "Unknown")
    namespace = os.getenv("POD_NAMESPACE", "default")
    image_version = os.getenv("IMAGE_VERSION", "1.0.0")

    return {
        "message": f"Hi! This is {pod_name} running in {namespace} namespace.",
        "pod_name": pod_name,
        "node_name": node_name,
        "namespace": namespace,
        "image_version": image_version,
        "status": "Service is running smoothly!"

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI microservice!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

