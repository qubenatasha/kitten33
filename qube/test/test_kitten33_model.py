#!/usr/bin/python
"""
Add docstring here
"""
import time
import unittest

import mock

from mock import patch
import mongomock


class Testkitten33Model(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("before class")

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def test_create_kitten33_model(self):
        from qube.src.models.kitten33 import kitten33
        kitten33_data = kitten33(name='testname')
        kitten33_data.tenantId = "23432523452345"
        kitten33_data.orgId = "987656789765670"
        kitten33_data.createdBy = "1009009009988"
        kitten33_data.modifiedBy = "1009009009988"
        kitten33_data.createDate = str(int(time.time()))
        kitten33_data.modifiedDate = str(int(time.time()))
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            kitten33_data.save()
            self.assertIsNotNone(kitten33_data.mongo_id)
            kitten33_data.remove()

    @classmethod
    def tearDownClass(cls):
        print("After class")


if __name__ == '__main__':
    unittest.main()
