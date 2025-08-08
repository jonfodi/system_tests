import uvicorn
from fastapi import FastAPI
from concurrent.futures import ProcessPoolExecutor
import asyncio
import math
import time

process_pool = ProcessPoolExecutor(max_workers=2)

app = FastAPI()

def cpu_intensive_task(n: int) -> dict:
    """
    This function runs in a separate process.
    It won't block the main FastAPI process.
    """
    start_time = time.time()
    
    # Simulate heavy computation
    result = 0
    for i in range(n):
        result += math.sin(i) * math.cos(i)
    
    end_time = time.time()
    
    return {
        "result": result,
        "computation_time": end_time - start_time,
        "iterations": n
    }

@app.get("/compute/{iterations}")
async def heavy_compute(iterations: int = 10_000_000):
    """
    CPU-heavy endpoint that won't block other requests.
    This will run in a separate process.
    """
    print(f"Starting computation with {iterations} iterations...")
    
    # This runs in separate process - main process stays free
    result = await asyncio.get_event_loop().run_in_executor(
        process_pool, cpu_intensive_task, iterations
    )
    
    print("Computation completed!")
    return result

@app.get("/light")
async def light_compute():
    return {"message": "Light computation completed!"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


