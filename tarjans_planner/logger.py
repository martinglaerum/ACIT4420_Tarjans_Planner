import os
import time
import datetime
from functools import wraps

    # Finds the absolute path to the current file's directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def timethis(func):
    
    # Wrapping function
    @wraps(func)
    def wrapper(*args, **kwargs):

        file_path = os.path.join(CURRENT_DIR, "time_log.txt") # Path to the log file
        start_time = time.time()  # Save the start time
        
        result = func(*args, **kwargs)  # Call the original function
        
        end_time = time.time()  # Save the start time
        execution_time = end_time - start_time
        
            # Print execution time
        print(f"Function {func.__name__} executed at: {datetime.datetime.now().replace(microsecond=0)}, execution time: {execution_time:.4f} seconds")
        
        # Save the execution time to the log file
        with open(file_path, "a") as f:
            f.write(f"Function {func.__name__} executed at: {datetime.datetime.now().replace(microsecond=0)}, execution time: {execution_time:.4f} seconds\n")
        
        return result
    return wrapper
