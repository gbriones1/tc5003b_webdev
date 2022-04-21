import pdb


def wrapper(func):
    print("Func init")
    return func

@wrapper
def main():
    print("Hello World")
    
main()