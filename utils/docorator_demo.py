import time
from functools import wraps


def log_call(func):
    """
    A simple decorator that logs when a function is called.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling function: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


def measure_time(func):
    """
    A decorator that measures how long a function takes to run.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"[TIMER] {func.__name__} executed in {duration:.4f} seconds")
        return result

    return wrapper


def repeat(times):
    """
    A decorator factory that repeats a function call N times.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for i in range(times):
                print(f"[REPEAT] Run {i + 1}/{times}")
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


# -------------------------
# Example usage
# -------------------------

@log_call
def greet(name):
    print(f"Hello, {name}!")


@measure_time
def slow_add(a, b):
    time.sleep(0.5)
    return a + b


@repeat(3)
def say_hi():
    print("Hi!")


if __name__ == "__main__":
    greet("Weipeng")
    print(slow_add(3, 5))
    say_hi()
