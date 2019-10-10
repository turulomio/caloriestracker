## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from time import time
from socket import create_connection
from logging import error, debug, warning

## allows you to measure the execution time of the method/function by just adding the @timeit decorator on the method.
## @timeit
def timeit(method):
    def timed(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()

        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed

## Checks if there is internet
def is_there_internet(method):
    def internet(*args, **kw):
        try:
            # connect to the host -- tells us if the host is actually
            # reachable
            create_connection(("www.google.com", 80))
            debug("There is Internet connection")
        except OSError:
            error("There is not Internet connection")
        return method(*args, **kw)
    return internet

## This is a decorator which can be used to mark functions
## as deprecated. It will result in a warning being emitted
## when the function is used
def deprecated(method):
    def new_func(*args, **kwargs):
        warning("Call to deprecated function {}.".format(method.__name__))
        return method(*args, **kwargs)
    return new_func


@is_there_internet
@deprecated
def testing_decorators1():
    for i in range(10):
        print(i)

@timeit
def testing_decorators2():
    for i in range(10):
        print(i)
        
if __name__ == "__main__":
    testing_decorators1()
    testing_decorators2()
