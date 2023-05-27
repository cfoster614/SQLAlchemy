from unittest import TestCase
from app import app

class FlaskTests(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        
    def test_home_route(self):
        """Check to make sure home route works"""
        with self.client:
            response = self.client.get('/users')
            self.assertEqual(response.status_code, 200)
            
    def test_new_user_route(self):
        """Check route brings to new user form"""
        with self.client:
            response = self.client.get('/users/new')
            self.assertEqual(response.status_code, 200)
    
    def test_user_details_route(self):
        """Clicking name should bring to page with user details"""
        with self.client:
            response = self.client.get('/users/{user_id}')
            self.assertEqual(response.status_code, 200)
    def test_user_edit_route(self):
        """Edit button should bring to page to edit user info"""
        with self.client:
            user_id = 1
            response = self.client.get(f'/users/{user_id}/edit')
            self.assertEqual(response.status_code, 200)
    def test_delete_redirect(self):
        """Deleting user should redirect to user list page"""
        with self.client:
            user_id = 1
            response = self.client.get(f'/users/{user_id}/delete')
            self.assertEqual(response.status_code, 302)