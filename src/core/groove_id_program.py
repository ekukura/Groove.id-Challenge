'''
Created on May 19, 2018

@author: emilykukura
'''

import os


def execute_update():
    pass


def launch_main_program():
    
    print("Main program launched")
    x = 5
    y = 6
    print("Performing a simple addition: {arg0} + {arg1} = {res}".format(arg0 = x, arg1 = y, res = x+y))


def run():
    
    #===========================================================================
    # version = {}
    # with open("version.py") as fp:
    #     exec(fp.read(), version)
    #     
    # print("The current version is {}".format(version['__version__']))
    #===========================================================================
    
    version_file_name = "version_info.txt"
    project_source_directory = os.getcwd()
    version_file_path = os.path.join(project_source_directory, version_file_name)
    print("version file path: {}".format(version_file_path))
    with open(version_file_path) as version_file:
        version = version_file.read().strip()
        print("version: {}".format(version))
    #here I want to check remote version from github
       
    #launch_main_program()


if __name__ == '__main__':
    
    run()