'''
Created on May 19, 2018

@author: emilykukura
'''

def perform_tasks():
    '''
    The main program code would go here. For now just doing a few simple tasks.
    '''
    x = 5
    y = 6
    print("Performing a simple addition: {arg0} + {arg1} = {res}".format(arg0 = x, arg1 = y, res = x+y))
    print([i for i in range(10)])
    

def launch(cur_version):
    '''
    :type cur_version: str
    :param cur_version: the current version number of the program
    '''
    print("Main program launched")
    perform_tasks()
    print("This is version {} of the program".format(cur_version))
