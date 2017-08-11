#!/usr/bin/env python
import subprocess
import unittest
import requests
import time
import json
from pprint import pprint

workingdir = '../'
host = '127.0.0.1'
port = '8181'


class SatelliteTest(unittest.TestCase):
    def setUp(self):
        self.response = requests.get('http://{}:{}/satellites'.format(host, port))

    def testResponseType(self):
        """ensure the response is a JSON array"""
        content = json.loads(self.response.content)
        self.assertIsInstance(content, list)

    def testResponseLength(self):
        """verify response is not 0 length"""
        content = json.loads(self.response.content)
        self.assertNotEqual(len(content), 0)

    def testFail(self):
        """assert that FAIL is not in the returned list"""
        content = json.loads(self.response.content)
        self.assertNotIn('FAIL', content)

    def testSO50(self):
        """assert that SO-50 is in the output"""
        content = json.loads(self.response.content)
        self.assertIn('SO-50', content)

    def testISS(self):
        """assert that ISS is in the returned list"""
        content = json.loads(self.response.content)
        self.assertIn('ISS', content)

    def tearDown(self):
        pass
        # self.process.kill()
        # self.output.close()


if __name__ == '__main__':
    with open('output.txt', 'w') as output:
        cmd = ['gunicorn',
               '-b', '{}:{}'.format(host, port),
               '--error-logfile', 'tests/gunicornout.txt',
               '--capture-output',
               'app']
        print('Starting the app')
        process = subprocess.Popen(cmd, cwd=workingdir, stdout=output)
        time.sleep(5)
        print('Running satellite endpoint tests')
        satSuite = unittest.TestLoader().loadTestsFromTestCase(SatelliteTest)
        foo = unittest.TextTestRunner(verbosity=0).run(satSuite)
        print('Shutting Down')
        process.terminate()
        process.wait()
