#it depends on the python can user function as args and return_val
# This is our decorator
'''
def simple_decorator(f):
    # This is the new function we're going to return
    # This function will be used in place of our original definition
    def wrapper():
        print "Entering Function"
        f()
        print "Exited Function"
 
    return wrapper
 
@simple_decorator 
def hello():
    print "Hello World"
hello()
'''
def use_logging(func):

    def wrapper():
        print("%s is running" % func.__name__)
        return func() 
    return wrapper

'''def foo():
    print('i am foo')

foo()
print("--------------")
foo = use_logging(foo) 
foo()                 
'''
#it also equal to ,it's syntactic sugar
#it ignores the foo=user_logging(foo)
#simply add a decorator to the defined place
@use_logging
def foo():
	print("i am foo")
foo()
