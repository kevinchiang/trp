import fastapi
from routes import task_result


app = fastapi.FastAPI()

app.include_router(task_result.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
