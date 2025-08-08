# CPU BOUND SYSTEM TESTS

Goal: analyze and test different methods for handling CPU-intensive requests within a web framework 

Problem
- CPU intensive tasks are long 
- they block the proces that runs the web app while the compute, blocking any other users from interacting with the app 

Constraints 
- await is only for I/O tasks (tasks that do not rely on the process' dedicated CPU)
- Pythons GIL prevents the use of threadding 

# Solution 1
- use a separate process for CPU intensive tasks 

Pros 
- solves the blocking of request for other users issue 

Cons 
- Memory overhead -> every new process requires duplication of all the app code and the bloat you don't think of when mocking an app :) 

