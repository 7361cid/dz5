import unittest
import requests
from multiprocessing import Process
from httpd import HTTPserver


def runserver():
    server = HTTPserver(root="DOCUMENT_ROOT")
    server.run()


# !!!! Мб нужны пау3ы между тестами
class RequestTests(unittest.TestCase):
    def setUp(self):
        self.process = Process(target=runserver)
        self.process.start()

    def tearDown(self) -> None:
        self.process.terminate()

    def test_basic_answer(self):
        response = requests.get('http://localhost:8080/httptest/dir2/page.html')
        print(f"response сщву {response}")
        print(f"response headers {response.headers}")
        print(f"response content {response.content}")




if __name__ == "__main__":
    unittest.main()
