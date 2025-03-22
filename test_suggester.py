import unittest
from suggester import Suggester, app

class TestSuggester(unittest.TestCase):
    def setUp(self):
        self.suggester = Suggester("ruwords.txt")

    def test_get_suggestions(self):
        result = self.suggester.get("ябл")
        self.assertEqual(result, ["яблоко", "яблоня"])

    def test_get_no_suggestions(self):
        result = self.suggester.get("xyz")
        self.assertEqual(result, [])

    def test_get_case_insensitive(self):
        result = self.suggester.get("Ябл")
        self.assertEqual(result, ["яблоко", "яблоня"])

    def test_get_partial_match(self):
        result = self.suggester.get("чер")
        self.assertEqual(result, ["черника", "черешня"])

    def test_get_limit_results(self):
        result = self.suggester.get("б")
        self.assertEqual(result, ["банан", "брусника", "боярышник"])

    def test_get_suggestions_count(self):
        result = self.suggester.get("б")
        self.assertEqual(len(result), 10, "Expected 10 suggestions, but got more.")

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_suggest_handler(self):
        response = self.app.get('/?w=ябл')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, ["яблоко", "яблоня"])

    def test_suggest_handler_no_results(self):
        response = self.app.get('/?w=xyz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_suggest_handler_case_insensitive(self):
        response = self.app.get('/?w=Ябл')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, ["яблоко", "яблоня"])

    def test_suggest_handler_partial_match(self):
        response = self.app.get('/?w=чер')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, ["черника", "черешня"])

    def test_suggest_handler_limit_results(self):
        response = self.app.get('/?w=б')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, ["банан", "брусника", "боярышник"])

if __name__ == '__main__':
    unittest.main()
