# CPU BOUND SYSTEM TESTS

Goal: analyze and test different methods for handling CPU-intensive requests within a web framework 

Problem
- CPU intensive tasks are long 
- they block the proces that runs the web app while the compute, blocking any other users from interacting with the app 

Constraints 
- await is only for I/O tasks (tasks that do not rely on the process' dedicated CPU)
- Pythons GIL prevents the use of threadding 

# Set Up 
git clone 
python -m venv venv 
source venv/bin/activate 
pip install -r requirements.txt
uvicorn main:app --reload

# Solution 1
use a separate process for CPU intensive tasks 

Pros 
- solves the blocking of request for other users issue 

Cons 
- Memory overhead -> every new process requires duplication of all the app code and the bloat you don't think of when mocking an app :) 

Test 
- curl http://127.0.0.1:8000/compute/100000000 
- curl http://127.0.0.1:8000/light
    - in a new terminal 
- observe how the light response gets returned while the heavy task is still computing 

# Solution 2
horizontal scaling 
- add memory resources for each 

Pros
- use many processes 
Cons
- cost scales linearly with number of requests 

# Solution 3
dont use python 
- Python's GIL only allows 1 thread to execute at a time 

oh did u ask what the GIL was??? im so glad 
the GIL is a way to prevent a variable from being updated differently in different threads
- a "race condition" (multiple lines of code running in parallel, "racing" towards completion) can cause the same variable to be updated differently
- this can cause memory leaks (when a program does not return the memory back to the OS) because it may be expecting a certain value for the variable before returning and the race condition can cause the value to be unknown 
- a "lock" (or "mutex") is a piece of code that prevents multiple threads from accesssing the same ressource at once. 
- to perform multithreading with locks, you need ... multiple locks
- but this can create deadlocks - 2 threads waiting for one another to execute 
- the GIL is a lock on the INTERPRETER --> its a rule that says any python code requires the interpreter lock to execute 
- interesting note: trying to implement multi-threading in python actually INCREASES execution time. because the GIL will only let you use 1 thread, and the time it takes to create, assign, and close processes takes more time
    - https://stackoverflow.com/questions/59811870/the-number-of-process-running-in-parallel-is-determined-by-the-number-of-physica
    - https://realpython.com/python-gil/

but ya. go has goroutines. rust has 

