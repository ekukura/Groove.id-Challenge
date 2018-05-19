'''
Created on May 19, 2018

@author: emilykukura
'''



def launch(cur_version):
    
    print("Main program launched")
    x = 5
    y = 6
    print("Performing a simple addition: {arg0} + {arg1} = {res}".format(arg0 = x, arg1 = y, res = x+y))
    print([i for i in range(12)])
    print("This is version {} of the program".format(cur_version))
