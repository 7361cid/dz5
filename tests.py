import unittest
import requests
from multiprocessing import Process
from httpd import HTTPserver


def runserver():
    server = HTTPserver(root="DOCUMENT_ROOT")
    server.run()


class TestSuite(unittest.TestCase):
    def setUp(self):
        self.process = Process(target=runserver)
        self.process.start()

    def tearDown(self) -> None:
        self.process.terminate()

    def test_basic_answer(self):
        response = requests.get('http://localhost:8000')
        print(response)
        print(response.text)

    def test_get_file(self):
        response = requests.get('http://localhost:8000/file.html')
        print(response)
        print(response.text)


if __name__ == "__main__":
    unittest.main()
