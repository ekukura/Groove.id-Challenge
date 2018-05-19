'''
Created on May 19, 2018

@author: emilykukura
'''

def execute_update():
    pass


def launch_main_program():
    
    print("Main program launched")
    x = 5
    y = 6
    print("Performing a simple addition: {arg0} + {arg1} = {res}".format(arg0 = x, arg1 = y, res = x+y))


def run():
    
    version = {}
    with open("version.py") as fp:
        exec(fp.read(), version)
        
    print(version['__version__'])
    
    
    #launch_main_program()


if __name__ == '__main__':
    
    run()