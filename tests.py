import os
import unittest
import time
import subprocess

file_path = os.path.dirname(os.path.abspath(__file__))


def runserver():
    os.system(f'python httpd.py -r {file_path}/http-test-suite-master')


def runtests():
    os.system(f'python {file_path}/http-test-suite-master/httptest.py')


class RequestTests(unittest.TestCase):
    def setUp(self):
        self.process = subprocess.Popen(f'python httpd.py -r {file_path}/http-test-suite-master'.split())
        self.process2 = subprocess.Popen(f'python {file_path}/http-test-suite-master/httptest.py'.split(), stdout=subprocess.PIPE)

    def tearDown(self) -> None:
        self.process.terminate()
        self.process2.terminate()

    def test_basic_answer(self):
        stdout = self.process2.communicate()[0]
        success = False
        for i in range(25):
            time.sleep(5)
            if b"OK" in stdout:
                success = True
                break
        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()
