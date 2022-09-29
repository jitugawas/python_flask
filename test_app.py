import unittest
import json
import app

BASE_URL = 'http://127.0.0.1:5000/users'
BAD_ITEM_URL = '{}/5'.format(BASE_URL)
GOOD_ITEM_URL = '{}/3'.format(BASE_URL)


class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def test_get_all(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 4)

    # def test_get_one(self):
    #     response = self.app.get(BASE_URL+"/1")
    #     data = json.loads(response.get_data())
    #     print(data['user_name'])
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['user_name'], 'test_name')

    # def test_item_not_exist(self):
    #     response = self.app.get("http://127.0.0.1:5000/users/5")
    #     self.assertEqual(response.status_code, 404)

    # def test_post(self):
    #     # missing value field = bad
    #     item = {"user_name": "test4_name"}
    #     response = self.app.post("http://127.0.0.1:5000/add",
    #                              data=json.dumps(item),
    #                              content_type='application/json')
    #     self.assertEqual(response.status_code, 404)

    # def test_update(self):
    #     item = {"user_name": "test_name","user_email":"test_name@gmail.com","user_password":"123456"}
    #     response = self.app.put(GOOD_ITEM_URL+"/1",
    #                             data=json.dumps(item),
    #                             content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.get_data())
    #     self.assertEqual(data['user_name'], "test1_name")

    # def test_delete(self):
    #     response = self.app.get('http://127.0.0.1:5000/delete/3')
    #     self.assertEqual(response.status_code, 404)
    #     print(response.status_code)
    #     response = self.app.get('http://127.0.0.1:5000/delete/5')
    #     print(response.status_code)
    #     self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()