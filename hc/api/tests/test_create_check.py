import json

from hc.api.models import Channel, Check
from hc.test import BaseTestCase


class CreateCheckTestCase(BaseTestCase):
    URL = "/api/v1/checks/"

    def setUp(self):
        super(CreateCheckTestCase, self).setUp()

    def post(self, data, expected_error=None):
        """Assert that the expected error is the response error"""
        r = self.client.post(self.URL, json.dumps(data),
                             content_type="application/json")

        if expected_error:
            string_content = r.content.decode("utf-8")
            json_content = json.loads(string_content)
            response_error = json_content.get("error")
            self.assertEqual(r.status_code, 400)
            self.assertIn(expected_error, response_error)

        return r

    def test_it_works(self):
        """Assert the expected last_ping and n_pings values"""
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })

        self.assertEqual(r.status_code, 201)

        doc = r.json()
        assert "ping_url" in doc
        self.assertEqual(doc["name"], "Foo")
        self.assertEqual(doc["tags"], "bar,baz")

        self.assertEqual(Check.objects.count(), 1)
        check = Check.objects.get()
        self.assertEqual(check.last_ping, None)
        self.assertEqual(check.n_pings, 0)
        self.assertEqual(check.name, "Foo")
        self.assertEqual(check.tags, "bar,baz")
        self.assertEqual(check.timeout.total_seconds(), 3600)
        self.assertEqual(check.grace.total_seconds(), 60)

    def test_it_accepts_api_key_in_header(self):
        """Make the post request with api_key in header and get the response"""
        payload = json.dumps({"name": "Foo"})
        r = self.client.post(self.URL, payload,
                             content_type='application/json', HTTP_X_API_KEY='abc')

        self.assertEqual(r.status_code, 201)

    def test_it_handles_missing_request_body(self):
<<<<<<< HEAD

=======
        
>>>>>>> 167b23a4f41a3653abdefdbaace0f59f92fc0628
        """Make the post request with a missing body and get the response"""
        r = self.client.post(self.URL, content_type="application/json")
        string_content = r.content.decode("utf-8")
        json_content = json.loads(string_content)
        self.assertEqual(r.status_code, 400)
<<<<<<< HEAD

=======
       
>>>>>>> 167b23a4f41a3653abdefdbaace0f59f92fc0628
        self.assertEqual(json_content.get("error"), "wrong api_key")

    def test_it_handles_invalid_json(self):
        """Make the post request with invalid json data type"""
        r = self.client.post(self.URL, "invalid data", content_type="application/json")
        string_content = r.content.decode("utf-8")
        json_content = json.loads(string_content)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json_content.get("error"), "could not parse request body")

    def test_it_rejects_wrong_api_key(self):
        """Assertion for wrong API key"""
        r = self.post({"api_key": "wrong"},
                  expected_error="wrong api_key")
        string_content = r.content.decode("utf-8")
        json_content = json.loads(string_content)
        self.assertEqual(json_content.get("error"), "wrong api_key")

    def test_it_rejects_non_number_timeout(self):
        """reject non number timeout"""
        r = self.post({"api_key": "abc", "timeout": "oops"},
                  expected_error="timeout is not a number")
        string_content = r.content.decode("utf-8")
        json_content = json.loads(string_content)
        self.assertEqual(json_content.get("error"), "timeout is not a number")

    def test_it_rejects_non_string_name(self):
        """test to reject a non string name"""
        r = self.post({"api_key": "abc", "name": False},
                  expected_error="name is not a string")
        string_content = r.content.decode("utf-8")
        json_content = json.loads(string_content)
        self.assertEqual(json_content.get("error"), "name is not a string")
<<<<<<< HEAD

=======
        
>>>>>>> 167b23a4f41a3653abdefdbaace0f59f92fc0628
    def test_it_assigns_channels(self):
        """Test for the assignment of channels"""
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60})
        check = Check.objects.get()
        self.assertTrue(check.assign_all_channels)
<<<<<<< HEAD

    def test_timeout_is_too_small(self):
        """Test for the timeout is too small when set to 1"""
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 1,
            "grace": 60})
        string_content = r.content.decode("utf-8")
        json_content = json.loads(string_content)
        self.assertEqual(json_content.get("error"), "timeout is too small")

    def test_timeout_is_too_large(self):
        """Test for the timeout is too large"""
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 720000,
            "grace": 60})
        string_content = r.content.decode("utf-8")
        json_content = json.loads(string_content)
        self.assertEqual(json_content.get("error"), "timeout is too large")
=======
        
    def test_timeout_is_too_small(self):
        """Test for the timeout is too small when set to 1"""
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 1,
            "grace": 60})
        string_content = r.content.decode("utf-8")
        json_content = json.loads(string_content)
        self.assertEqual(json_content.get("error"), "timeout is too small")
        
    def test_timeout_is_too_large(self):
        """Test for the timeout is too large"""
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 720000,
            "grace": 60})
        string_content = r.content.decode("utf-8")
        json_content = json.loads(string_content)
        self.assertEqual(json_content.get("error"), "timeout is too large")

>>>>>>> 167b23a4f41a3653abdefdbaace0f59f92fc0628
