import secrets
import string
import uuid
import datetime as dt

DUMMY_ID = str(uuid.UUID('00000000-0000-0000-0000-000000000000'))
AUTHORS_URL = '/authors/'
BOOKS_URL = '/books'
AUTH_URL = '/auth/'


class TestApi:
    """TEST API"""
    jwt_token = None
    author_1_id = author_1 = None
    book_1_id = book_1 = None
    book_2_id = book_2 = None

    def test_login_jwt(self, test_client):
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        ret = test_client.post(AUTH_URL, query_string={'user_email': 'test@email.com', 'password': password})
        ret_val = ret.json
        assert ret.status_code == 200
        TestApi.jwt_token = ret_val.pop('access_token')

    def test_authors_post(self, test_client):
        TestApi.author_1 = {
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": dt.datetime(1958, 10, 2).strftime('%Y-%m-%d')
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
