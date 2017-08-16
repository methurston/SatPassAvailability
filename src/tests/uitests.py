#!/usr/bin/env python

import subprocess
import unittest
from selenium import webdriver
from time import sleep
from pprint import pprint


class UITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://localhost:8181/index.html")
        cls.test_user = 'W1AW'

    def setUp(self):
        reset_btn = self.driver.find_element_by_id('resetUserBtn')
        reset_btn.click()

    # def testPageTitle(self):
    #     """Verify page title. Simple case to ensure expected page is loaded"""
    #     self.assertEqual(self.driver.title, 'N7DFL - Sat Pass Availability')
    #
    # def testResetButton(self):
    #     """Verify data entered in callsign field is cleared with reset"""
    #     id_field = self.driver.find_element_by_id('callsign')
    #     id_field.send_keys('FOO')
    #     reset_button = self.driver.find_element_by_id('resetUserBtn')
    #     reset_button.click()
    #     id_field = self.driver.find_element_by_id('callsign')
    #     self.assertEqual(id_field.get_attribute('value'), '')
    #
    # def testSeedGoodUser(self):
    #     """Enter a known good user for further testing"""
    #     id_field = self.driver.find_element_by_id('callsign')
    #     id_field.send_keys(self.test_user)
    #     submit = self.driver.find_element_by_id('getUserBtn')
    #     submit.click()
    #     result_div = self.driver.find_element_by_id('usertitle')
    #     if result_div.text.find('{} not found'.format(self.test_user)) != -1:
    #         add_btn = self.driver.find_element_by_id('addUserBtn')
    #         add_btn.click()
    #     grid_square = self.driver.find_element_by_id('gridsquare').get_attribute('value')
    #     self.assertEqual(grid_square, 'FN31pr')
    #
    # def testFindUser(self):
    #     """when entering a known good username, verify the expected data is returned to the UI"""
    #     id_field = self.driver.find_element_by_id('callsign')
    #     get_user_btn = self.driver.find_element_by_id('getUserBtn')
    #     id_field.send_keys(self.test_user)
    #     get_user_btn.click()
    #     tz_field = self.driver.find_element_by_id('timezone')
    #     self.assertEqual(tz_field.get_attribute('value'), 'America/New_York')
    #
    # def testEnterAvailability(self):
    #     """Verify submitting a timeslot is successful"""
    #     id_field = self.driver.find_element_by_id('callsign')
    #     get_user = self.driver.find_element_by_id('getUserBtn')
    #     id_field.send_keys(self.test_user)
    #     get_user.click()
    #     days = self.driver.find_elements_by_css_selector('div.dayLeft input[type="checkbox"]')
    #     for day in days:
    #         day.click()
    #     time = self.driver.find_element_by_id('start_time')
    #     duration = self.driver.find_element_by_id('duration')
    #     time.send_keys('1300PM')
    #     duration.send_keys('3600')
    #     duration.send_keys('\t')  # send a tab to fire the blur event
    #     store_btn = self.driver.find_element_by_id('addSlotBtn')
    #     self.assertNotEqual(store_btn.get_attribute('disabled'), 'true')
    #     store_btn.click()
    #     slot_title = self.driver.find_element_by_id('slottitle')
    #     self.assertEqual(slot_title.text, 'Timeslot stored')

    def testDeleteTimeslot(self):
        """Verify that deleting a timeslot removes it from the UI"""
        id_field = self.driver.find_element_by_id('callsign')
        get_user = self.driver.find_element_by_id('getUserBtn')
        id_field.send_keys(self.test_user)
        get_user.click()
        show_timeslots = self.driver.find_element_by_id('allheader')
        show_timeslots.click()
        timeslot_rows = self.driver.find_elements_by_xpath("//div[@id='storedinfo']/table/tbody/tr")  #find all rows
        cells = timeslot_rows[1].find_elements_by_tag_name('td')
        delete_id = cells[0].text
        cells[3].click()
        self.driver.switch_to.alert.accept()
        new_show_timeslots = self.driver.find_element_by_id('allheader')
        new_show_timeslots.click()
        new_show_timeslots.click()  # why twice? Handle focus better
        print('Title: {}'.format(self.driver.title))
        new_timeslot_rows = self.driver.find_elements_by_xpath("//div[@id='storedinfo']/table/tbody/tr")  #find all rows
        print(len(new_timeslot_rows))
        for row in new_timeslot_rows[1:]:
            cells = row.find_elements_by_tag_name('td')
            print(cells[0].text)
            self.assertNotEqual(cells[0].text, delete_id)





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