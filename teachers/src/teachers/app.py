from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from teachers.crew import Teachers
from teachers.redis_service import redis_service
from teachers.request_handler import process_aiml_request
import asyncio
import os

# Environment configuration
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(env_path)

app = FastAPI()

redis_listener_task = None
subscription_ready = asyncio.Event()


class Query(BaseModel):
    input: str
    current_year: int = 2026
    mode: str = "pro"  # "pro" or "lite"


@app.on_event("startup")
async def startup_event():
    global redis_listener_task
    
    try:
        await redis_service.connect()
        redis_listener_task = asyncio.create_task(listen_for_requests())
        await asyncio.wait_for(subscription_ready.wait(), timeout=5.0)
        print("✅ AIML service ready and listening for requests")
        
    except asyncio.TimeoutError:
        print("⚠️ Warning: Redis subscription not confirmed within timeout")
    except Exception as e:
        print(f"❌ Failed to initialize Redis: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    global redis_listener_task
    
    try:
        if redis_listener_task:
            redis_listener_task.cancel()
            try:
                await redis_listener_task
            except asyncio.CancelledError:
                pass
        
        await redis_service.disconnect()
        print("✅ Redis service disconnected")
        
    except Exception as e:
        print(f"Error during shutdown: {e}")


async def listen_for_requests():
    try:
        await redis_service.subscribe_and_listen(
            'aiml:requests',
            process_aiml_request,
            subscription_ready
        )
    except asyncio.CancelledError:
        print("Request listener cancelled")
    except Exception as e:
        print(f"Error in request listener: {e}")


@app.post("/query")
def query(query: Query):
    inputs = {
        'topic': query.input,
        'current_year': str(query.current_year)
    }
    
    if query.mode.lower() == "lite":
        r = Teachers().simple_crew()
    else:
        r = Teachers().crewcall()
        
    result = r.kickoff(inputs=inputs)
    return {"response": result.raw}


@app.get("/")
def home():
    return {
        "message": "Welcome to the study portal",
        "status": "Redis pub/sub enabled",
        "redis_connected": redis_service.check_connection()
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "redis_connected": redis_service.check_connection()
    }
