# Groove.id-Challenge
Solution to Groove.id Challenge

The problem is to create a program which will update itelf. 
My solution relies on the following:

(1) The code manager is updating the files version_info.txt and update_list.json
  (a) version_info.txt just contains the version number -- the launcher.py file uses this to determine if an update is needed
  (b) update_list.json is a python dictionary which stores lists of three types of file updates: files that are new (on the repo in newest version), files that have been updated since last version, and files that should be deleted (files that were on old versions and are not in new versions)
    -NOTE: this may be tedious and could cause some problems if a user missed updates 
    FOR EXAMPLE: say if a new file was added in version 2.0 and hasn't been modified since, and the client goes straight from version 1.9 to 2.1 (missing the 2.0 update). In this case the new file would not be added on
the clients version (though if it had been modified in the update to version 2.1 it WOULD still be added b/c of how the program handles a file that is in the modified list but not in the local program file system)
  - One way around this would be just to, on every update, delete all local program files and then add all files in github repo for most recent version. However, if a program was large and contained many files, this would not be a good solution if only a few small updates were made.
  - Another (better) solution would be to keep a list of all files that are present in the current version, along with a modified list. Then check this list of all files against the client program files. If there are files that are in the current version that are not in the client version, add them, and then also perform all updates for files in the modified list
  
(2) The implementation of the updates requres that the file structure of the program for the client is the same as that stored in the GitHub repo. E.g. for this specific program all source files, and the version_info.txt
and update_list.json files, are located in the src/core package. This would need to be the case on the client systems as well.


####################################################################################

The program itself is launched from launcher.py, which will check if an update is needed or not. 
If needed, an update will be performed (including, if necessary, an update to launcher.py itself).
After the update is performed (or if no update was needed), launcher.py will call the main program 
(groove_id_program) - explicitly  main_program.launch(__version__)  (where main_program is an alias for groove_id_program) is called. main_program performs a few tasks and prints the current version id.

####################################################################################

Other concerns/areas for improvement:

(1) The fact that the client has access to the entire update script is probably not the best idea
for a program. They could easily corrupt this file so that it no longer is able to receive the desired updates.
It would probably be better to run the update from an executable file (In thoery, this executable could probably just pull an update.py python script from the web which is very similar to launcher.py, and then execute this script using e.g. python udpate.py )
(2) More unit-tests would certainly be needed for a production-quality program. In particular:
  (a) tests to ensure platform independence
  (b) tests to ensure that the updates are actually performing as expected
(3) Production-quality code should probably have a bit more exception handling than what I have here

