from threading import Thread


def run_in_background(func):
    """
        Apply this decorator on any function to run that function as a background process
    """

    def decorator(*args, **kwargs):
        t = Thread(target=func, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return decorator
