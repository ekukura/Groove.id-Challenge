'''
Created on May 19, 2018

@author: emilykukura
'''
import unittest
import core.launcher as launcher

class Test(unittest.TestCase):


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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_version_greater']
    unittest.main()