import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

class TestFiles(unittest.TestCase):
    def test_various(self):
        #print(get_files_info("calculator", "."))
        #print(get_files_info("calculator", "pkg"))
        #print(get_files_info("calculator", "/bin"))
        #print(get_files_info("calculator", "../"))
        print(get_file_content("calculator", "lorem.txt"))
        print(get_file_content("calculator", "main.py"))
        print(get_file_content("calculator", "pkg/calculator.py"))
        print(get_file_content("calculator", "/bin/cat"))

if __name__ == "__main__":
    unittest.main()