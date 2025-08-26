import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# .strftime('%m_%d_%Y_%H_%M_%S') : Formats that datetime into a string like: "08_26_2025_23_45_10".
# Result: "08_26_2025_23_45_10.log" - every run of the program creates a unique log filename based on current time.

logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE) # Result path: /home/user/project/logs/08_26_2025_23_45_10.log

os.makedirs(logs_path,exist_ok=True) # Creates directories at the given path if they don’t already exist.
# exist_ok=True : Prevents error if the folder already exists.

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    # This sets up the logging system:
    # filename=LOG_FILE_PATH : All logs will be written to that file.
    
    # format="..." :  Defines how each log message looks.
    # %(asctime)s : Timestamp when the log entry was created.
    # %(lineno)d : Line number in the code where the log was generated.
    # %(name)s : Logger’s name (usually the module name).
    # %(levelname)s : The log level (INFO, ERROR, WARNING, etc.).
    # %(message)s : The actual log message.
    
    # level=logging.INFO → Sets the minimum log level. Messages at INFO or above (WARNING, ERROR, CRITICAL) 
    # will be logged, DEBUG won’t.

)


