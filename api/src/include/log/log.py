from functools import wraps

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Synchronous call: {func.__name__}")
        try: 
            result = func(*args, **kwargs)
            print(f"Synchronous result {func.__name__}:\n{result}")
            return result
        except Exception as e:
            print(f"Synchronous execution error {func.__name__}:\n{e}")
            return None   
    return wrapper

def async_logger(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"Asynchronous call: {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            print(f"Asynchronous result {func.__name__}:\n{result}")
            return result
        except Exception as e:
            print(f"Asynchronous execution error {func.__name__}:\n{e}")
            return None  
    return wrapper