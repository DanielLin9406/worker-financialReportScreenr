import inspect


def dumpArgs(func):
    """Decorator to print function call details - parameters names and effective values.
    """
    def wrapper(*args, **kwargs):
        func_args = inspect.signature(func).bind(*args, **kwargs).arguments
        func_args_str = ', '.join('{} = {!r}'.format(*item)
                                  for item in func_args.items())
        print(f'{func.__module__}.{func.__qualname__} ( {func_args_str} )')
        result = func(*args, **kwargs)
        print(f'{func.__module__}.{func.__qualname__} Return Result: \n {result}')
        return result
    return wrapper
