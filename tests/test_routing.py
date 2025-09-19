import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from router.router import QueryRouter

class TestRouting(unittest.TestCase):

    def test_simple_query(self):
        router = QueryRouter()
        query = "What is the capital of France?"
        result = router.route_query_and_return_response(query)
        self.assertEqual(result.model_name, "gemini-1.5-flash")

if __name__ == '__main__':
    unittest.main()

