from django.test import TestCase

# Create your tests here.

def test_dashboard(self):
    response = self.client.get('/dashboard/')
    self.assertEqual(response.status_code, 200)
    
    # Check that the rendered context contains 5 customers.
    self.assertEqual(len(response.context['customers']), 5)
    
    