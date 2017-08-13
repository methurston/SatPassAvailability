#!/usr/bin/env python
import subprocess
import unittest
import requests
import time
import json
import os


workingdir = '../'
host = '127.0.0.1'
port = '8181'


class SatelliteTest(unittest.TestCase):
    """Verify the response from the /satellites endpoint"""
    def setUp(self):
        self.response = requests.get('http://{}:{}/satellites'.format(host, port))

    def testResponseType(self):
        """ensure the response is a JSON array"""
        content = json.loads(self.response.content)
        self.assertIsInstance(content, list)

    def testOKstatus(self):
        """Verify 200OK is returned"""
        self.assertEqual(self.response.status_code, 200)

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


class UserTests(unittest.TestCase):
    """Validate put and get methods on the /user endpoint
    User is an object with the keys:
            'lat': None,
            'long': None,
            'callsign': 'test',
            'street_address': '404 S 8th st. Boise, Idaho',
            'timezone': 'America/Denver',
            'grid': 'DN13'
    """

    def setUp(self):
        self.endpoint = 'http://{}:{}/user/'.format(host, port)

    def tearDown(self):
        pass

    def testMissingUser(self):
        """Verify when a bad user name is provided, nothing is returned"""
        response = requests.get('{}baduser'.format(self.endpoint, port))
        self.assertEqual(response.status_code, 404)

    def testSendNotJSON(self):
        """Verify a contentype error is received when payload is not json"""
        user = {
            'lat': None,
            'long': None,
            'callsign': 'test',
            'street_address': '404 S 8th st. Boise, Idaho',
            'timezone': 'America/Denver',
            'grid': 'DN13'
        }
        headers = {'content_type': 'text/plain'}
        response = requests.post('{}{}'.format(self.endpoint, user.get('callsign')), data=user, headers=headers)
        message = json.loads(response.content)
        self.assertEqual(response.status_code, 415)
        self.assertEqual(message.get('title'), 'Unsupported media type')
        self.assertEqual(message.get('description'), 'Content must be sent as application/json')

    def testCreateGoodUser(self):
        user = {
            'lat': None,
            'long': None,
            'callsign': 'test',
            'street_address': '404 S 8th st. Boise, Idaho',
            'timezone': 'America/Denver',
            'grid': 'DN13'
        }
        response = requests.post('{}{}'.format(self.endpoint, user.get('callsign')), json=user)
        self.assertEqual(response.status_code, 204)

    def testExpectedKeys(self):
        """test to ensure GET 'test' user returns expected keys.  
           Note that street_address is only used to calculate lat/long and not stored or
           returned"""
        response = requests.get('{}{}'.format(self.endpoint, 'test'))
        userdict = json.loads(response.content)
        expected = sorted(['lat', 'lon', 'callsign', 'timezone', 'gridsquare', 'elevation'])
        self.assertEqual(expected, sorted(userdict.keys()))

    def testMissingLat(self):
        """Verify correct key is returned when missing lat"""
        user = {
            'callsign': 'test',
            'long': -116.206325,
            'elevation': 555,
            'timezone': 'America/Denver',
            'grid': 'DN13'
        }
        response = requests.post('{}{}'.format(self.endpoint, user.get('callsign')), json=user)
        message = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message.get('error'), "Missing Property")
        self.assertEqual(message.get('property name'), "lat")

    def testMissingLong(self):
        """Verify correct key is returned in error payload when long is missing"""
        user = {
                'callsign': 'test',
                'lat': 43.612988,
                'elevation': 555,
                'timezone': 'America/Denver',
                'grid': 'DN13'
            }
        response = requests.post('{}{}'.format(self.endpoint, user.get('callsign')), json=user)
        message = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message.get('error'), "Missing Property")
        self.assertEqual(message.get('property name'), "long")

    def testMissingElevation(self):
        """Verify update is successful when elevation is missing"""
        user = {
            'callsign': 'test',
            'lat': 43.612988,
            'long': -116.206325,
            'street_address': '404 S 8th St. Boise, ID 83702',
            'timezone': 'America/Denver',
            'grid': 'DN13'
        }
        response = requests.post('{}{}'.format(self.endpoint, user.get('callsign')), json=user)
        self.assertEqual(response.status_code, 204)

    def testMissingStreetAddress(self):
        """Verify correct key is returned in error payload when street address is missing"""
        user = {
            'callsign': 'test',
            'lat': 43.612988,
            'long': -116.206325,
            'elevation': 555,
            'timezone': 'America/Denver',
            'grid': 'DN13'
        }
        response = requests.post('{}{}'.format(self.endpoint, user.get('callsign')), json=user)
        message = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message.get('error'), "Missing Property")
        self.assertEqual(message.get('property name'), "street_address")

    def testMissingGrid(self):
        """Verify correct key is returned in error payload when grid is missing"""
        user = {
            'callsign': 'test',
            'lat': 43.612988,
            'long': -116.206325,
            'elevation': 555,
            'street_address': '404 S 8th St. Boise, ID 83702',
            'timezone': 'America/Denver'
        }
        response = requests.post('{}{}'.format(self.endpoint, user.get('callsign')), json=user)
        message = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message.get('error'), "Missing Property")
        self.assertEqual(message.get('property name'), "grid")

    def testMissingTimezone(self):
        """Verify correct key is returned in error payload when grid is missing"""
        user = {
            'callsign': 'test',
            'lat': 43.612988,
            'long': -116.206325,
            'elevation': 555,
            'street_address': '404 S 8th St. Boise, ID 83702'
        }
        response = requests.post('{}{}'.format(self.endpoint, user.get('callsign')), json=user)
        message = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message.get('error'), "Missing Property")
        self.assertEqual(message.get('property name'), "timezone")

    def testUpdateLatLon(self):
        """Change the address on a user, verify lat/lon are updated as expected"""
        user = {
            'lat': None,
            'long': None,
            'callsign': 'test',
            'street_address': '700 W. Jefferson St. Boise, ID 83702',
            'timezone': 'America/Denver',
            'grid': 'DN13'
        }
        update_response = requests.post('{}{}'.format(self.endpoint, user.get('callsign')), json=user)
        self.assertEqual(update_response.status_code, 204)
        get_response = requests.get('{}{}'.format(self.endpoint, user.get('callsign')))
        new_user = json.loads(get_response.content)
        self.assertEqual(new_user.get('lat'), 43.6178216)
        self.assertEqual(new_user.get('lon'), -116.1995185)


if __name__ == '__main__':
    with open('output.txt', 'w') as output:
        gunoutput = 'tests/gunicornout.txt'
        cmd = ['gunicorn',
               '-b', '{}:{}'.format(host, port),
               '--error-logfile', gunoutput,
               '--capture-output',
               'app']
        print('Starting the app')
        process = subprocess.Popen(cmd, cwd=workingdir, stdout=output)
        time.sleep(5)
        results = {}
        print('Running satellite endpoint tests')
        satSuite = unittest.TestLoader().loadTestsFromTestCase(SatelliteTest)
        results['satellites'] = unittest.TextTestRunner(verbosity=0).run(satSuite)
        print('Running user endpoint tests')
        userSuite = unittest.TestLoader().loadTestsFromTestCase(UserTests)
        results['user'] = unittest.TextTestRunner(verbosity=0).run(userSuite)
        failingsuites = [key for key in results.keys() if len(results[key].failures) != 0]
        if len(failingsuites) == 0:
            print('All suites pass')
            print('Cleaning up')
            os.remove(gunoutput.split('/')[1])
        else:
            print('{} suite(s) failed'.format(', '.join(failingsuites)))
        print('Shutting Down')
        process.terminate()
        process.wait()
