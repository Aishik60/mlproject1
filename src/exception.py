# search for exceptions in Python documentation to get a better idea

import sys
from src.logger import logging

# We’ll use sys.exc_info() to access the current exception info (type, value, traceback) when we’re inside an except block.

def error_message_detail(error,error_detail:sys): # error_detail:sys: a type hint saying you’ll pass the sys module.
    _,_,exc_tb=error_detail.exc_info()
    
    # Calls sys.exc_info() to get a triple (exc_type, exc_value, exc_traceback).
    # _ discards the type and value; keeps exc_tb (a traceback object).
    # Precondition: this should be called inside an except block. Outside of it, 
    # exc_info() returns (None, None, None) and exc_tb would be None.
    
    file_name=exc_tb.tb_frame.f_code.co_filename

    # Digs into the traceback to get the filename of the code object where the exception occurred (at this traceback frame).
    # exc_tb.tb_frame : the stack frame.
    # .f_code : the code object for that frame.
    # .co_filename : absolute (or source) filename string.
    
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
     file_name,exc_tb.tb_lineno,str(error))

    return error_message

# We define our own exception type that wraps the original error with the formatted details. Inherits from Exception.     

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    # Constructor takes : error_message - you typically pass the caught exception (e) or a string.
    # error_detail - again, you pass the sys module so it can call exc_info().
    # Calls base Exception’s __init__ so the exception still has a message.
    # Builds and stores the formatted message by calling the helper.   
    def __str__(self):
        return self.error_message
    
#if __name__=="__main__" :
#    
#    try:
#        a=1/0
#    except Exception as e:
#        logging.info("Divide by zero error")
#        raise CustomException(e,sys)
    

        