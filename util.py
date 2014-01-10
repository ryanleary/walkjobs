import time


def time_dec(func):
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print func.func_name + " took {0:.2f}ms".format(1000*(time.clock()-t))
        return res

    return wrapper