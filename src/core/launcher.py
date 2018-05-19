'''
Created on May 19, 2018

@author: emilykukura
'''

import os, re, importlib
import urllib.request

import core.groove_id_program as main_program
from shutil import copyfile

#TODO: modularize
#TODO: add unittests (figure out how to simulate windows and linux, if possible)
#TODO: add documentation for all methods
#TODO: implement execute_update method
#TODO: add gitignore

def update_file(old_file_path, new_file_path):
    '''
    Update file at location old_file_path to contain contents of new_file_path
    '''
    old_file_full_path = os.path.abspath(old_file_path)
    new_file_full_path = os.path.abspath(new_file_path)
        
    #old_file_directory = os.path.dirname(old_file_full_path) #get from old_file_paths parent
    #old_file_name = os.path.basename(old_file_full_path) #need to store this , will put copied file in a file with this name
    
    copyfile(src = new_file_full_path, dst = old_file_full_path)

    
    
def execute_update():
    
    print("execute_update called")
    #handle for mac, windows, and linux
    
    #first figure out how to handle on mac


def get_version(text):
    
    version_match = re.search("(?<=version_id = )\d+(.\d+)+(?=\s|$)", text)
    #this ensures 'version_id = ' comes before the value parsed, and that afterwords there
    #is either a space or end of line (so, e.g. 1.0.12..3 won't be matched b/c of the double dot
    #In general, ensures the version_id parsed is a dot-separated string of integers
    if version_match:
        return float(version_match.group(0))
    else:
        return None
    

def get_updated_version_id():
    
    
    url = "https://raw.githubusercontent.com/ekukura/Groove.id-Challenge/master/src/core/version_info.txt"
    f = urllib.request.urlopen(url)
    raw_bytes = f.read()      
    raw_text = str(raw_bytes, 'utf-8')
    url_version = get_version(raw_text)
        
    return url_version


def get_current_version_id():
    
    version_file_name = "version_info.txt"
    project_source_directory = os.getcwd()
    version_file_path = os.path.join(project_source_directory, version_file_name)
    with open(version_file_path) as version_file:
        version_info = version_file.read().strip()
        version = get_version(version_info)
        
    return version


def version_greater(version1, version2):
    '''
    :returns: true if version1 > version2 and false otherwise
    '''
    #first validate version1 and version2 in correct form
    #TODO: this is not actually correct, versions WONT be floats unless only of form x.y
    # -- implement function to determine if newer  -- but for now this is fine
    if version1 > version2:
        return True
    else:
        return False
        

def update_needed():
    global __version__, __master_version__
    
    update_needed = False
    
    __version__ = get_current_version_id()
    __master_version__ = get_updated_version_id() #want to check remote version from github

    if __master_version__ and __version__: #if both these are NOT None
        
        if version_greater(__master_version__,__version__):
            update_needed = True
            
    else: #TODO: find better name for Exception here; possibly separate handling
        raise Exception("unable to extract current or master version in appropriate form")
    
    return update_needed

    
def run():
    
    need_update = update_needed()
    
    print("current program version: {}".format(str(__version__)))
    print("master program version = ", str(__master_version__))
    
    if need_update:
        print("\nTime to update!")
        #TODO: (possibly) BEFORE updating, send message to user indicating they will 
        #need update and asking for permission/warning it will destroy old files and 
        #replace them
        execute_update()
        importlib.reload(main_program)  #this is to capture update
    else:
        print("\nProgram is up to date")
        
    main_program.launch() 
    #TODO: check if this runs in BOTH cases -- may need to RELOAD main_program module
    # can do this via import importlib: importlib.reload(main_program)
        

if __name__ == '__main__':
    
    run()