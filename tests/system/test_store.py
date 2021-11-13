import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json

class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post('/store/test')
                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'id': 1, 'name': 'test', 'items': []}, json.loads(resp.data))

    def test_create_duplicate_Store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                resp = client.post('/store/test')
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual(json.loads(resp.data), {'message': "A store with name 'test' already exists."})



    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                # or StoreModel('test').save_to_db()
                resp = client.delete('/store/test')  # get, post, delete, put, patch
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), ({'message': 'Store deleted'}))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.get('/store/test')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(resp.json, {'id': 1, 'name': 'test', 'items': []})


    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/store/test1')
                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual(resp.json, {'message': 'Store not found'})

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', 19.99, 1).save_to_db()
                resp = client.get('/store/test')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'id': 1, 'name': 'test', 'items': [{
                    'name': 'test_item',
                    'price': 19.99
                }]})

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                StoreModel('test1').save_to_db()
                resp = client.get('/stores')
                self.assertDictEqual({'stores': [{'id': 1, 'name': 'test', 'items': []}, {'id': 2, 'name': 'test1', 'items': []}]},
                                     json.loads(resp.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', 19.99, 1).save_to_db()
                ItemModel('test_item1', 19.55, 1).save_to_db()
                resp = client.get('/stores')
                # print(resp.status_code, json.loads(resp.data))
                self.assertDictEqual({'stores': [{'id': 1, 'name': 'test', 'items': [{'name': 'test_item', 'price': 19.99}, {'name': 'test_item1', 'price': 19.55}]}]},
                                     json.loads(resp.data))
                self.assertEqual(resp.status_code, 200)