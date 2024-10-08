import secrets
import string
import uuid
import datetime as dt

DUMMY_ID = str(uuid.UUID('00000000-0000-0000-0000-000000000000'))
AUTHORS_URL = '/authors/'
BOOKS_URL = '/books'
USERS_URL = '/users/signUp'
AUTH_URL = '/login/'


class TestApi:
    """TEST API"""
    jwt_token = None
    user_1_email = user_1 = None
    author_1_id = author_1 = None
    book_1_id = book_1 = None
    book_2_id = book_2 = None

    def test_create_user(self, test_client):
        TestApi.user_1 = {
            "email": ''.join(secrets.choice(string.ascii_letters) for i in range(12)),
            "first_name": "user_fname",
            "last_name": "user_lname"
        }
        ret = test_client.post(USERS_URL, json=TestApi.user_1)
        ret_val = ret.json
        TestApi.user_1_email = ret_val.pop('email')
        assert ret.status_code == 201

    def test_login_jwt(self, test_client):
        ret = test_client.post(AUTH_URL, query_string={'user_email': TestApi.user_1_email})
        ret_val = ret.json
        assert ret.status_code == 200
        TestApi.jwt_token = ret_val.pop('access_token')

    def test_authors_post(self, test_client):
        TestApi.author_1 = {
            "first_name": "auther_fname",
            "last_name": "auther_lname",
            "birth_date": dt.datetime(1999, 10, 2).strftime('%Y-%m-%d')
        }
        headers_jwt = {
            'Authorization': 'Bearer {}'.format(TestApi.jwt_token)
        }

        ret = test_client.post(AUTHORS_URL, json=TestApi.author_1, headers=headers_jwt)
        assert ret.status_code == 201
        ret_val = ret.json
        TestApi.author_1_id = ret_val.pop('id')
        ret_val.pop('created_at')
        ret_val.pop('updated_at')
        assert ret_val == TestApi.author_1

    def test_books_post(self, test_client):
        TestApi.book_1 = {
            'title': 'test_title',
            'author_id': TestApi.author_1_id,
            "category": "random",
            "price": 50,
            "release_date": "2024-10-05T16:12:50"
        }
        headers_jwt = {
            'Authorization': 'Bearer {}'.format(TestApi.jwt_token),
        }

        ret = test_client.post(f"{BOOKS_URL}/new", json=TestApi.book_1, headers=headers_jwt)
        assert ret.status_code == 201
        ret_val = ret.json
        TestApi.book_1_id = ret_val.pop('id')
        ret_val.pop('created_at')
        ret_val.pop('updated_at')
        assert ret_val == TestApi.book_1

    def test_books_get_id(self, test_client):
        ret = test_client.get(f"{BOOKS_URL}/get/" + TestApi.book_1_id)
        assert ret.status_code == 200
        ret_val = ret.json
        ret_val.pop('id')
        ret_val.pop('created_at')
        ret_val.pop('updated_at')
        assert ret_val == TestApi.book_1

    def test_books_put404(self, test_client):
        headers_jwt = {
            'Authorization': 'Bearer {}'.format(TestApi.jwt_token)
        }
        # PUT wrong ID -> 404
        ret = test_client.put(
            f"{BOOKS_URL}/edit/" + DUMMY_ID, json=TestApi.book_1, headers=headers_jwt
        )
        assert ret.status_code == 404
