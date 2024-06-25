import unittest
from app.contract_utils import highlight_changes

class TestContractUtils(unittest.TestCase):

    def test_highlight_changes(self):
        original = "This is a test."
        updated = "This is a modified test."
        result = highlight_changes(original, updated)
        self.assertIn('<span style="color:green;">modified test.</span>', result)

if __name__ == '__main__':
    unittest.main()
