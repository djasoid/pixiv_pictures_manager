import logging
import time
import os
from datetime import datetime

class Log:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_handler = None
    file_handler = None

    @staticmethod
    def init(log_folder = "./log/") -> None:
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        log_file = os.path.join(log_folder, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

        Log.console_handler = logging.StreamHandler()
        Log.console_handler.setLevel(logging.DEBUG)
        Log.console_handler.setFormatter(formatter)
        Log.logger.addHandler(Log.console_handler)
        
        Log.file_handler = logging.FileHandler(log_file, encoding='utf-8')
        Log.file_handler.setLevel(logging.INFO)
        Log.file_handler.setFormatter(formatter)
        Log.logger.addHandler(Log.file_handler)
        
    @staticmethod
    def debug(msg: str) -> None:
        Log.logger.debug(msg)
    
    @staticmethod
    def info(msg: str) -> None:
        Log.logger.info(msg)
    
    @staticmethod
    def warning(msg: str) -> None:
        Log.logger.warning(msg)
    
    @staticmethod
    def error(msg: str) -> None:
        Log.logger.error(msg, exc_info=True)
    
    @staticmethod
    def critical(msg: str) -> None:
        Log.logger.critical(msg, exc_info=True)

def log_execution(level: str, start_message: str | None, end_message: str | None): # log decorator
    def decorator(func):
        def wrapper(*args, **kwargs):
            method = func.__name__
            try:
                if start_message is not None:
                    f_start_message = start_message.format(method=method, args=args, kwargs=kwargs)
                    if level == "Debug":
                        Log.debug(f_start_message)
                    elif level == "Info":
                        Log.info(f_start_message)
                    elif level == "Warning":
                        Log.warning(f_start_message)

                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                execution_time = end_time - start_time
                
                if end_message is not None:                
                    f_end_message = end_message.format(
                        method=method, 
                        args=args, 
                        kwargs=kwargs, 
                        result=result, 
                        execution_time=execution_time
                    )
                    if level == "Debug":
                        Log.debug(f_end_message)
                    elif level == "Info":
                        Log.info(f_end_message)
                    elif level == "Warning":
                        Log.warning(f_end_message)
                    
                return result
            
            except Exception as e:
                Log.error(f"Error in {method}: {e}")
                raise
            
        return wrapper
    return decorator

