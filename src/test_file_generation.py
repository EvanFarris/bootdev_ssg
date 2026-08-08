import unittest
from file_generation import extract_title


class TestFileGeneration(unittest.TestCase):
    def test_extract_header(self):
        header = extract_title("# Hello")
        self.assertEqual(header, "Hello")

if __name__ == "__main__":
    unittest.main()