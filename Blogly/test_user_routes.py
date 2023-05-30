from unittest import TestCase
from app import app
from models import User

class UserRoutes(TestCase):
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
        with self.client:
            """Check redirect after submitting form"""
            res = self.client.post('/users/new', data={'first_name' : 'Mr. Test', 'last_name' : 'Test'})
            self.assertEqual(res.status_code, 302)
            
    
    def test_user_details_route(self):
        """Clicking name should bring to page with user details"""
        with self.client:
            response = self.client.get('/users/1')
            self.assertEqual(response.status_code, 200)
            html = response.get_data(as_text = True)
            self.assertIn('<h1>Mr. Test Test</h1>', html)

    def test_user_edit_route(self):
        """Edit button should bring to page to edit user info"""
        with self.client:
            get_resp = self.client.get('/users/1/edit')
            html = get_resp.get_data(as_text = True)
            self.assertEqual(get_resp.status_code, 200)
            self.assertIn('<h1>Edit a user</h1>', html)
        with self.client:
            post_resp = self.client.post('/users/1/edit', data={'user_id' : '1'})
            self.assertEqual(post_resp.status_code, 302)

    # def test_delete_redirect(self):
    #     """Deleting user should redirect to user list page"""
    #     with self.client:
    #         user_id = 1
    #         response = self.client.get(f'/users/{user_id}/delete')
    #         self.assertEqual(response.status_code, 302)