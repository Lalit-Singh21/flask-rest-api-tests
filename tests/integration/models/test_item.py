from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            #below line StoreModel("..").save_to_db() is required to not to have
            # integrity error for foreign key store_id in items table
            StoreModel('test_store').save_to_db()

            #not an item test so will have to move below test to store test
            #self.assertIsNotNone(StoreModel.find_by_name('test_store'))

            item = ItemModel('test', 19.99, 1)

            self.assertIsNone(ItemModel.find_by_name('test'),
                              "Found an item with name {}, but expected not to.".format(item.name))

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name('test'))

            item.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name('test'))


    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(item.store.name, 'test_store')
            self.assertEqual(item.store_id, 1)
            self.assertEqual(item.store.id, 1)


