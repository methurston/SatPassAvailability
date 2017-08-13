#!/usr/bin/env python

import subprocess
import unittest
from selenium import webdriver
from time import sleep


class UITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://localhost:8181/index.html")

    def testPageTitle(self):
        """Verify page title. Simple case to ensure expected page is loaded"""
        self.assertEqual(self.driver.title, 'N7DFL - Sat Pass Availability')

    def testResetButton(self):
        """Verify data entered in callsign field is cleared with reset"""
        id_field = self.driver.find_element_by_id('callsign')
        id_field.send_keys('FOO')
        reset_button = self.driver.find_element_by_id('resetUserBtn')
        reset_button.click()
        id_field = self.driver.find_element_by_id('callsign')
        self.assertEqual(id_field.text, '')

    def testFindUser(self):
        """when entering a known good username, verify the expected data is returned to the UI"""
        id_field = self.driver.find_element_by_id('callsign')
        get_user_btn = self.driver.find_element_by_id('getUserBtn')
        id_field.send_keys('N7DFL')
        get_user_btn.click()
        tz_field = self.driver.find_element_by_id('timezone').text
        print('TZ TEst')
        self.assertEqual(tz_field, 'America/Boise')


    @classmethod
    def tearDownClass(cls):
        # cls.driver.close()
        pass

if __name__ == '__main__':
    with open('httpoutput.txt', 'w') as output:
        print('Starting HTTP server')
        http_cmd = ['python',
                    '-m', 'http.server',
                    '8181']
        http_working_dir = '../../html'
        http_process = subprocess.Popen(http_cmd, cwd=http_working_dir, stdout=output)
        print('Starting API server')
        gunoutput = 'tests/gunicornout.txt'
        host = '127.0.0.1'
        port = 8000
        api_cmd = ['gunicorn',
                   '-b', '{}:{}'.format(host, port),
                   '--error-logfile', gunoutput,
                   '--capture-output',
                   'app']
        api_working_dir = '../'
        api_process = subprocess.Popen(api_cmd, cwd=api_working_dir, stdout=output)
        sleep(3)
        ui_suite = unittest.TestLoader().loadTestsFromTestCase(UITests)
        results = unittest.TextTestRunner(verbosity=0).run(ui_suite)
        print('Shutting down http server')
        http_process.kill()
        http_process.wait()
        print('Shutting down API server')
        api_process.kill()
        api_process.wait()