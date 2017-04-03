#!/usr/bin/python
"""
Add docstring here
"""
import os
import time
import unittest

import mock
from mock import patch
import mongomock


with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    os.environ['KITTEN33_MONGOALCHEMY_CONNECTION_STRING'] = ''
    os.environ['KITTEN33_MONGOALCHEMY_SERVER'] = ''
    os.environ['KITTEN33_MONGOALCHEMY_PORT'] = ''
    os.environ['KITTEN33_MONGOALCHEMY_DATABASE'] = ''

    from qube.src.models.kitten33 import kitten33
    from qube.src.services.kitten33service import kitten33Service
    from qube.src.commons.context import AuthContext
    from qube.src.commons.error import ErrorCodes, kitten33ServiceError


class Testkitten33Service(unittest.TestCase):
    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        context = AuthContext("23432523452345", "tenantname",
                              "987656789765670", "orgname", "1009009009988",
                              "username", False)
        self.kitten33Service = kitten33Service(context)
        self.kitten33_api_model = self.createTestModelData()
        self.kitten33_data = self.setupDatabaseRecords(self.kitten33_api_model)
        self.kitten33_someoneelses = \
            self.setupDatabaseRecords(self.kitten33_api_model)
        self.kitten33_someoneelses.tenantId = "123432523452345"
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            self.kitten33_someoneelses.save()
        self.kitten33_api_model_put_description \
            = self.createTestModelDataDescription()
        self.test_data_collection = [self.kitten33_data]

    def tearDown(self):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            for item in self.test_data_collection:
                item.remove()
            self.kitten33_data.remove()

    def createTestModelData(self):
        return {'name': 'test123123124'}

    def createTestModelDataDescription(self):
        return {'description': 'test123123124'}

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setupDatabaseRecords(self, kitten33_api_model):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            kitten33_data = kitten33(name='test_record')
            for key in kitten33_api_model:
                kitten33_data.__setattr__(key, kitten33_api_model[key])

            kitten33_data.description = 'my short description'
            kitten33_data.tenantId = "23432523452345"
            kitten33_data.orgId = "987656789765670"
            kitten33_data.createdBy = "1009009009988"
            kitten33_data.modifiedBy = "1009009009988"
            kitten33_data.createDate = str(int(time.time()))
            kitten33_data.modifiedDate = str(int(time.time()))
            kitten33_data.save()
            return kitten33_data

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_post_kitten33(self, *args, **kwargs):
        result = self.kitten33Service.save(self.kitten33_api_model)
        self.assertTrue(result['id'] is not None)
        self.assertTrue(result['name'] == self.kitten33_api_model['name'])
        kitten33.query.get(result['id']).remove()

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_kitten33(self, *args, **kwargs):
        self.kitten33_api_model['name'] = 'modified for put'
        id_to_find = str(self.kitten33_data.mongo_id)
        result = self.kitten33Service.update(
            self.kitten33_api_model, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['name'] == self.kitten33_api_model['name'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_kitten33_description(self, *args, **kwargs):
        self.kitten33_api_model_put_description['description'] =\
            'modified for put'
        id_to_find = str(self.kitten33_data.mongo_id)
        result = self.kitten33Service.update(
            self.kitten33_api_model_put_description, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['description'] ==
                        self.kitten33_api_model_put_description['description'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_kitten33_item(self, *args, **kwargs):
        id_to_find = str(self.kitten33_data.mongo_id)
        result = self.kitten33Service.find_by_id(id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_kitten33_item_invalid(self, *args, **kwargs):
        id_to_find = '123notexist'
        with self.assertRaises(kitten33ServiceError):
            self.kitten33Service.find_by_id(id_to_find)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_kitten33_list(self, *args, **kwargs):
        result_collection = self.kitten33Service.get_all()
        self.assertTrue(len(result_collection) == 1,
                        "Expected result 1 but got {} ".
                        format(str(len(result_collection))))
        self.assertTrue(result_collection[0]['id'] ==
                        str(self.kitten33_data.mongo_id))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_not_system_user(self, *args, **kwargs):
        id_to_delete = str(self.kitten33_data.mongo_id)
        with self.assertRaises(kitten33ServiceError) as ex:
            self.kitten33Service.delete(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_ALLOWED)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_by_system_user(self, *args, **kwargs):
        id_to_delete = str(self.kitten33_data.mongo_id)
        self.kitten33Service.auth_context.is_system_user = True
        self.kitten33Service.delete(id_to_delete)
        with self.assertRaises(kitten33ServiceError) as ex:
            self.kitten33Service.find_by_id(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_FOUND)
        self.kitten33Service.auth_context.is_system_user = False

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_item_someoneelse(self, *args, **kwargs):
        id_to_delete = str(self.kitten33_someoneelses.mongo_id)
        with self.assertRaises(kitten33ServiceError):
            self.kitten33Service.delete(id_to_delete)
