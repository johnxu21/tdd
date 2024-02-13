"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# import the unit under test - counter
from src.counter import app

# import the file that contains the status codes
from src import status


class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        result = self.client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update a counter"""
        # 1. Make a call to Create a counter
        result = self.client.post('/counters/foobar')

        # 2. Ensure that it returned a successful return code.
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # 3. Check the counter value as a baseline
        baseline = self.client.get('/counters/foobar')
        baseline = baseline.json['foobar']

        # 4. Make a call to Update the counter that you just created.
        result = self.client.put('/counters/foobar')

        # 5. Ensure that it returned a successful return code.
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        updated = self.client.get('/counters/foobar')
        updated = updated.json['foobar']

        # 6. Check that the counter value is one more than the baseline you measured in step 3.
        self.assertEqual(updated, baseline + 1)

        result = self.client.put('/counters/barbar')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)


    def test_read_counter(self):
        """It should return the counter"""
        # 1. Create a counter and ensure it is a success
        result = self.client.post('/counters/barfoo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        # 2. Update counter for testing
        for x in range(3):
            result = self.client.put('/counters/barfoo')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        # 3. Read the counter and ensure success
        read = self.client.get('/counters/barfoo')
        self.assertEqual(read.status_code, status.HTTP_200_OK)
        # 4. Check counter == 3 (testing)
        count = read.json['barfoo']
        self.assertEqual(count, 3)
        result = self.client.get('/counters/foobar')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_counter(self):
        """It should delete the counter"""
        # 1. Create a counter and ensure it is a success
        result = self.client.post('/counters/foofoo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        # 2. delete the counter
        delete = self.client.delete('/counters/foofoo')
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)
        # 3. Test for non-deleted  counter
        result = self.client.post('/counters/barbar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)
