'''
Created on May 19, 2018

@author: emilykukura
'''
import unittest
import core.launcher as launcher
from urllib.error import HTTPError


class Test(unittest.TestCase):

    def test_get_file_basename_from_mac_path(self):
        
        res = launcher.get_file_basename_from_relative_url("src/abc/dog.txt")
        self.assertEqual(res, "dog.txt")
        

    def test_version_greater(self):
        
        versioning_pair_tests = [("4", "3", True) , ("1.2.4", "1.2.3", True), 
                                 ("1.2.4", "1.2.3.3", True),  ("1.2.4", "1.3.4", False), 
                                 ("1.2.3.3", "1.2.3", True), ("1.2.3", "1.2.3.3", False)]
    
        for res_tuple in versioning_pair_tests:
            with self.subTest():
                v1 = res_tuple[0]
                v2 = res_tuple[1]
                self.assertTrue(launcher.version_greater(v1, v2) == res_tuple[2]) 
        
        
    def test_get_version(self):
        
        res = launcher.get_version("version_id = 1.0.12")
        self.assertEqual(res, "1.0.12")
        
        
    def test_is_valid_version(self):
        
        versions_valid_pairs = [("1.2.4", True),("4", True),
                               ("1.2..4", False),(" 1.2.4", False)]
        
        for pair in versions_valid_pairs:
            self.assertTrue(launcher.is_valid_version(pair[0]) == pair[1])
       
       
    def test_update_modified_file_error(self):
        
        base_github_url = "https://raw.githubusercontent.com/ekukura/Groove.id-Challenge/master"
        invalid_path = "src/core/nonexistent.txt"
        
        with self.assertRaises(HTTPError):
            launcher.update_file(base_github_url, invalid_path)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_version_greater']
    unittest.main()