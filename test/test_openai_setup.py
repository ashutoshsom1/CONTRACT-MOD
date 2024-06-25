import unittest
from unittest.mock import patch
from app.openai_setup import update_contract

class TestOpenAISetup(unittest.TestCase):

    @patch('app.openai_setup.agent_executor.invoke')
    def test_update_contract(self, mock_invoke):
        mock_invoke.return_value = {'output': 'Updated contract content.'}
        original_contract = "Original contract content."
        instructions = "Modify the contract."
        updated_contract = update_contract(original_contract, instructions)
        self.assertEqual(updated_contract, 'Updated contract content.')

if __name__ == '__main__':
    unittest.main()
