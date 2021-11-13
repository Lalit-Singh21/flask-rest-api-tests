from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        #for authorisation , request to contain an access token
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_req = client.post('/auth',
                                       data=json.dumps({'username': 'test', 'password': '1234'}),
                                       headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_req.data)['access_token']
                self.header = {'Authorization': f'JWT {auth_token}'}


    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                #@jwt_required() checks for authorisation and if not found returns 401
                self.assertEqual(resp.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers=self.header)
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                # @jwt_required() checks for authorisation and if not found returns 401
                resp = client.get('/item/test', headers=self.header)
                # print(resp.status_code)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test', 'price': 19.99})
                self.assertEqual(resp.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.delete('/item/test')#, headers=self.header)
                print(json.loads(resp.data))
                print(resp.status_code)
                self.assertDictEqual(json.loads(resp.data), {'message': 'Item deleted'})
                self.assertEqual(resp.status_code, 200)

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.post('item/test_item', data={'price': 19.99, 'store_id': 1})
                # print(json.loads(resp.data))
                # print(resp.status_code)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test_item', 'price': 19.99})
                self.assertEqual(resp.status_code, 201)

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 17.99, 1).save_to_db()
                resp = client.post('item/test_item', data={'price': 17.99, 'store_id': 1})
                # print(json.loads(resp.data))
                # print(resp.status_code)
                self.assertDictEqual(json.loads(resp.data), {'message': "An item with name 'test_item' already exists."})
                self.assertEqual(resp.status_code, 400)

    #create item with put
    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                resp = client.put('item/test_item', data={'price': 19.99, 'store_id': 1})
                # print(json.loads(resp.data))
                # print(resp.status_code)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test_item', 'price': 19.99})
                self.assertEqual(resp.status_code, 200)

    #  update item when already existing with put
    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 17.99, 1).save_to_db()
                self.assertEqual(ItemModel.find_by_name('test_item').price, 17.99)
                resp = client.put('item/test_item', data={'price': 19.99, 'store_id': 1})
                # print(json.loads(resp.data))
                # print(resp.status_code)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test_item', 'price': 19.99})
                self.assertEqual(resp.status_code, 200)

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                StoreModel('test_store2').save_to_db()
                ItemModel('test_item', 17.99, 1).save_to_db()
                ItemModel('test_item2', 5.99, 2).save_to_db()
                resp = client.get('/items')
                # print(json.loads(resp.data))
                # print(resp.status_code)
                self.assertDictEqual(json.loads(resp.data),
                                     {'items': [{'name': 'test_item', 'price': 17.99},
                                                {'name': 'test_item2', 'price': 5.99}]})

                self.assertEqual(resp.status_code, 200)
