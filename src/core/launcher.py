'''
Created on May 19, 2018

@author: emilykukura
'''

import os, sys
import re
import importlib
import json
import urllib.request
from urllib.error import HTTPError

import core.groove_id_program as main_program


#TODO: (1) Exception handling 
#TODO: (2) add explanation to README with info on assumptions of program (e.g. structure)
#    and other details 
#TODO: (3) make sure to mention security concerns with this method, how may be better 
#    to create different executable files for each platform and have it call the 
#    executable instead (ALT, maybe since launcher not to be changed by 
#    user, it could be DIRECTLY read from github and used? Think about this more
#    also mention list of what would add to improve (e.g. tests to ensure platform
#    independence, and that updates actually operate as expected) (POSSIBLY JUST MAKE
#    A FILE LISTING AREAS FOR IMPROVEMENT / CONCERNS instead of directly in e-mail body)
#    - should really have separate modified and new file methods, and modified
#    - should check to make sure that file is also on local path


def get_file_basename_from_relative_url(relative_path):
    '''
    
    :param relative_path: of form xxx/xxx/xxx/file_name (e.g. relative URL path form)
    :type relative_path: str
    
    :returns file_name
    '''
    
    components = relative_path.split("/")
    file_name = components[-1]

    return file_name 


def update_file(github_basepath, relative_path, is_new = False): 
    '''
    :param github_basepath: base url for raw data files contained in the master branch on GitHub repo
    :type github_basepath: str
    :param relative_path: string of form src/core/file_name 
        (since currently ALL files in src/core package)
    :type relative_path: str
    
    Assumes same file structure on GitHub and locally.
    If is_new = False, updates local version of file_name to a copy of the version of file_name on GitHub repo.
    If is_new = True will just create a file with name file_name where expected.
    '''
    
    print("updating the file: ", relative_path)
    full_github_url = os.path.join(github_basepath, relative_path)

    try:
        f = urllib.request.urlopen(full_github_url)
    except HTTPError as e:
        print("\nError while attempting to open the url {}\n".format(full_github_url), 
              file=sys.stderr)
        raise(e)
    else:
        raw_bytes_from_git = f.read() 
          
        target_filename = get_file_basename_from_relative_url(relative_path)
        target_dir = os.path.dirname(os.path.abspath(target_filename))
        
        os.chdir(target_dir)
        
        if not is_new: #e.g. is a modified file
            file_exists = os.path.isfile(target_filename)  #add code to ensure that the file is also located in this path
            print("file_exists = ", file_exists)
            if not file_exists:
                print("\nWarning, the file {} does not exist locally, and so it was created, not modified\n"
                      .format(target_filename), file=sys.stderr)
   
        with open(target_filename, "wb") as local_file:
            local_file.write(raw_bytes_from_git)  


def delete_file(relative_path):
    '''
    :param relative_path: string of form src/core/file_name 
        (since currently ALL files in src/core package)
    :type relative_path: str
    
    Assumes same file structure on GitHub and locally.
    Deletes the file_name from the local program.
    '''    
    target_filename = get_file_basename_from_relative_url(relative_path)
    target_dir = os.path.dirname(os.path.abspath(target_filename))
    
    os.chdir(target_dir)   
    os.remove(target_filename)
    print("File {} removed from program\n".format(target_filename))
    

def json_read_dict(json_path):
    '''
    :param json_path: location of json file to read from
    :type json_path: str
    
    :returns: the dictionary contained in the json file 
    '''
    with open(json_path, 'r') as json_file:
        main_dict = json.load(json_file)
                
    return main_dict
    
        
def execute_update(json_update_list_file = "update_list.json"):
    '''
    :param json_update_list_file: file containing a dictionary with the files that are new
        since last updated, modified since last update, and have been removed since last update
    :type json_update_list_file: str
    '''
    print("Updating...")
    
    #First pull most recent update_list from github to get accurate information about
    #what needs to be updated
    base_github_url = "https://raw.githubusercontent.com/ekukura/Groove.id-Challenge/master"
    update_file(base_github_url, "src/core/" + json_update_list_file)
     
    #next read the information about what to be updated from the update_list json file
    update_info = json_read_dict(json_update_list_file) 
    new_files = update_info['new files']
    modified_files = update_info['modified files']
    deleted_files = update_info['deleted files']    
    
    if 'launcher updated' in sys.argv: #this means we have already updated the launcher.py file
        modified_files.remove("src/core/launcher.py")
        
    print("Will be adding the new files: ", new_files)
    print("Will be updating the files: ", modified_files) 
    print("Will be deleting the files: ", deleted_files)
    
    if "src/core/launcher.py" in modified_files:
        #in this case, update launcher, then re-launch launcher.py to update remaining files
        update_file(base_github_url, "src/core/launcher.py")
        print("Re-launching launcher.py...")
        os.execv(sys.executable, ['python'] + sys.argv + ['launcher updated'])
      
    for path in modified_files:
        update_file(base_github_url, path)
    for path in new_files:
        update_file(base_github_url, path)
    for path in deleted_files:
        delete_file(path)
        
    print("\nProgram Updated.\n")    


def get_version(text):
    '''
    :type text: str
    :returns: extracted version_id from the input string text
    :rtype: str
    
    Example: get_version("version_id = 1.2.4 ") = "1.2.4"
    
    '''
    version_match = re.search("(?<=version_id = )\d+(.\d+)*(?=\s|$)", text)
    #this ensures 'version_id = ' comes before the value parsed, and that afterwords there
    #is either a space or end of line (so, e.g. 1.0.12..3 won't be matched b/c of the double dot
    #In general, ensures the version_id parsed is a dot-separated string of integers
    if version_match:
        return version_match.group(0).strip()
    else:
        return None
    

def get_updated_version_id():
    '''
    :returns: the version id stored in the version_info.txt file on github repo
    '''
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


def is_valid_version(version_str):
    '''
    :type version_str: str
    :return true if and only if version_str is a validly-formatted version id
    '''
    if not version_str: #e.g. if version_str == None
        return False
    
    version_format = re.compile("^\d+(.\d+)*$")
    version_valid = version_format.match(version_str)
    if version_valid: #e.g. version_valid is NOT None, so match made
        return True
    else:
        return False


def version_greater(version1, version2):
    '''
    :type version1: str
    :type version2: str
    :returns: true if version1 > version2 and false otherwise   
    
    Example:
    version_greater(1.2.4, 1.2.3) = True
    version_greater(1.2.4, 1.2.3.3) = True
    version_greater(1.2.4, 1.3.4) = False
    version_greater(1.2.3.3, 1.2.3) = True
    version_greater(1.2.3, 1.2.3.3) = False
    '''
    
    #first validate version1 and version2 in correct form
    if is_valid_version(version1) and is_valid_version(version2):
        #get first integer value before dot, if one greater than other done, else remove 
        cur_v1_match = re.match("\d+", version1)
        cur_v2_match = re.match("\d+", version2)
        cur_v1_val = int(cur_v1_match.group(0))
        cur_v2_val = int(cur_v2_match.group(0))
        
        if cur_v1_val > cur_v2_val:
            return True
        elif cur_v1_val < cur_v2_val:
            return False
        else: #so cur_v1_val = cur_v2_val
            #handle base case where at end of one of versions and STILL match, e.g. if v1 = 2.3.3 and v2 = 2.3.3.5
            if (version1.isdigit() or version2.isdigit()):  
                if version1.isdigit(): 
                    #then have that they are equal until v1's last digit, so either they are equal or v2 is greater (has further sections)
                    return False
                else: #so version2 isdigit and version1 IS NOT, e.g. version 1 has further sections
                    return True
               
            else:
            #these give ending indexes of the current section of version
                cur_v1_end = cur_v1_match.span()[1] 
                cur_v2_end = cur_v2_match.span()[1]
                return version_greater(version1[cur_v1_end + 1:], version2[cur_v2_end + 1:])
           
    else:
        raise ValueError("versions given do not match the correct version format")
 

def update_needed():
    '''
    Determines whether or not an update is needed by checking GitHub repo version against 
    version stored in local version_info.txt file
    '''
    global __version__, __master_version__
    
    update_needed = False
    
    __master_version__ = get_updated_version_id() #want to check remote version from github
    __version__ = get_current_version_id()

    if is_valid_version(__master_version__) and is_valid_version(__version__): 
        
        if version_greater(__master_version__,__version__):
            update_needed = True
            
    else: 
        if not is_valid_version(__master_version__):
            raise Exception("unable to extract version from github repo in expected format")
        else: #__version__ invalid
            raise Exception("unable to extract version from local version_info.txt in expected format")            
            
    return update_needed

    
def run():
    
    #check for update
    global __version__, __master_version__
    need_update = update_needed()
    
    print("\ncurrent program version: {}".format(str(__version__)))
    print("master program version = ", str(__master_version__))
    
    if need_update:
        execute_update()
        importlib.reload(main_program)  #this is to capture update's changes to the main_program
        __version__ = get_current_version_id()
    else:
        print("\nProgram is up to date")
        
    #once reach this point, have either updated already or don't need an update  
    main_program.launch(__version__) 

        

if __name__ == '__main__':
    
    run()

