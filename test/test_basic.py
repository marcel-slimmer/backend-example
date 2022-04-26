import unittest


class TestExample(unittest.TestCase):

    def test_answer(self):
        assert 2 + 3 == 5


if __name__ == '__main__':
    unittest.main()
