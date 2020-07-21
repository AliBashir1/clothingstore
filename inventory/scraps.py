def decorater_funtions(orignal_functions):
    def wrapper_functions():
        print("wrapper_function executed before {} function ".format(orignal_functions.__name__))
        return orignal_functions()
    return wrapper_functions

# this is equalt to display = decorater_function(display)
@decorater_funtions
def display():
    print("This is a display function")

display()


def test():
    a= 2
    b=3
    return a,  b


a, b = test()

print(a,b)