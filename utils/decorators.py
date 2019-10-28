import cProfile
import pstats
import io
import time
from multiprocessing.pool import ThreadPool
from multiprocessing.context import TimeoutError
from functools import wraps


def profiler(report='profiler.txt'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            pr = cProfile.Profile()
            pr.enable()
            my_result = func(*args, **kwargs)
            pr.disable()
            # s = io.BytesIO()
            with open(report, 'w+') as f:
                stats = pstats.Stats(pr, stream=f)
                stats.sort_stats('cumtime')
                stats.print_stats()
                # f.write(f.getvalue())
            return my_result
        return wrapper
    return decorator


def print_execution_time(f):
    @wraps(f)
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        delta = end - start
        print('Execution time: {:>6.2f}s ({})'.format(delta, f.__name__))
        return result
    return f_timer


def interrupt_after(max_timeout):
    """Timeout decorator, parameter in seconds."""
    def timeout_decorator(item):
        """Wrap the original function."""
        @wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator
