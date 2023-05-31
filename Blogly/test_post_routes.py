from unittest import TestCase
from app import app
 

class PostRoutes(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_new_post(self):
        """Check route to create new post"""
        with self.client:
            get_resp = self.client.get('/users/1/posts/new')
            self.assertEqual(get_resp.status_code, 200)

            post_resp = self.client.post('/users/1/posts/new', data={'title' : 'test', 'content' : 'test', 'user_id' : '1'})
            self.assertEqual(post_resp.status_code, 302)
    
    def test_post_route(self):
        """Should show post content"""
        with self.client:
            resp = self.client.get('/post/1')
            self.assertEqual(resp.status_code, 200)

    def test_edit_post(self):
        with self.client:
            get_resp = self.client.get('/post/1/edit')
            self.assertEqual(get_resp.status_code, 200)

            post_resp = self.client.post('/post/1/edit', data={'changed_title' : 'Title change', 'changed_content' : 'Content change'})
            self.assertEqual(post_resp.status_code, 302)

    def test_delete_post(self):
        """Test if deleting a post works"""
        with self.client:
            resp = self.client.get('/post/1/delete')
            self.assertEqual(resp.status_code, 302)
       
             
            