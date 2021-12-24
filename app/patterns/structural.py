import time


def profile(func):
    def wrapper_timeit(*args, **kwargs):
        start_time = time.perf_counter()
        res = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f'[PROFILE]: Finished {func.__name__!r} in {run_time:.4f} secs')
        return res

    return wrapper_timeit
