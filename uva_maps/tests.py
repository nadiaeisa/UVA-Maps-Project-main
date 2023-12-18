from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user
from .models import Feedback, PlaceRating
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class indexTestClass(TestCase):
    def test_index(self):
        response = self.client.get(reverse("route"))
        self.assertEqual(response.status_code, 302)


class routeTestClass(TestCase):
    def test_route_load(self):
        response = self.client.get(reverse("route"))
        self.assertEqual(response.status_code, 302)


class mapTestClass(TestCase):
    def test_map_load(self):
        response = self.client.get(reverse("map"))
        self.assertEqual(response.status_code, 302)


class requestLocationTestClass(TestCase):
    def test_map_load(self):
        response = self.client.get(reverse("user_feedback"))
        self.assertEqual(response.status_code, 200)


class approveLocationTestClass(TestCase):
    def test_map_load(self):
        response = self.client.get(reverse("admin_approval"))
        self.assertEqual(response.status_code, 302)


class FeedbackModelTest(TestCase):
    @classmethod
    def setUp(self):
        self.test_model = Feedback.objects.create(place="Rice Hall", address="85 Engineer's Way, Charlottesville, VA 22903", justification="A lot of students study here", description="The Computer Science building", rating = 4)
    
    def test_name_label(self):
        self.assertEqual(self.test_model.place, 'Rice Hall')
    
    def test_address_label(self):
        self.assertEqual(self.test_model.address, "85 Engineer's Way, Charlottesville, VA 22903")

    def test_justification_label(self):
        self.assertEqual(self.test_model.justification, "A lot of students study here")

    def test_description_label(self):
        self.assertEqual(self.test_model.description, "The Computer Science building")

    def test_rating_label(self):
        self.assertEqual(self.test_model.rating, 4)

    def test_status_choices(self):
       approved_feedback = Feedback.objects.create(status= "APPROVED")
       rejected_feedback = Feedback.objects.create(status= "REJECTED")
       pending_feedback = Feedback.objects.create(status= "PENDING")
       self.assertEqual(approved_feedback.status, "APPROVED") 
       self.assertEqual(rejected_feedback.status, "REJECTED") 
       self.assertEqual(pending_feedback.status, "PENDING") 
    
    def test_model_str_representation(self):
        self.assertEqual(str(self.test_model), 'Rice Hall')


class UVAMapsTestClass(TestCase):
    def setUp(self):
        google_app = SocialApp.objects.create(
               provider='google',
               name='Google',
               client_id='xxx.apps.googleusercontent.com',
               secret='xxx',
           )
           
        self.superuser = User.objects.create_superuser(
            username='test',
            email='admin@example.com',
            password='password'
        )

        self.user = User.objects.create_superuser(
            username='test2',
            email='notadmin2@example.com',
            password='password2'
        )

        SocialAccount.objects.create(
            user=self.superuser,
            provider=google_app.provider,
            uid='test_google_uid',
           )
        
    def test_google_api_login(self):
        self.client.login(username='test', password='password')
        response = self.client.get(reverse('uva_maps:user'))
        self.assertEqual(response.status_code, 200)

    def test_google_api_logout(self):
        self.client.login(username='test', password='password')
        response = self.client.get(reverse('uva_maps:user'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(reverse('uva_maps:user'))
        self.assertEqual(response.status_code, 302)

    def test_request_location(self):
        self.client.login(username='test', password='password')
        feedback_data = {
            'place': 'Test Place',
            'address': 'Test Address',
            'justification': 'Test Justification',
        }
        url = reverse('uva_maps:user_feedback')
        response = self.client.post(url, feedback_data)
        response2 = self.client.get(reverse('uva_maps:admin_approval'))
        self.assertContains(response2, "Place: Test Place")
    
    def test_accept_request(self):
        self.client.login(username='test', password='password')
        self.feedback = Feedback.objects.create(
            place='Test Place',
            address='Test Address',
            justification='Test Justification',
            status=Feedback.PENDING
        )
        url = reverse('uva_maps:approve_feedback', args=[self.feedback.id])
        response = self.client.post(url)
        updated_feedback = get_object_or_404(Feedback, pk=self.feedback.id)
        self.assertEqual(updated_feedback.status, Feedback.APPROVED)

    def test_reject_request(self):
        self.client.login(username='test', password='password')
        self.feedback = Feedback.objects.create(
            place='Test Place',
            address='Test Address',
            justification='Test Justification',
            status=Feedback.PENDING
        )
        url = reverse('uva_maps:reject_feedback', args=[self.feedback.id])
        response = self.client.post(url)
        deleted_feedback = Feedback.objects.filter(pk=self.feedback.id)
        self.assertQuerysetEqual(deleted_feedback, [])


class RatingTestClass(TestCase):
    def test_submit_rating(self):
        self.client.login(username='test', password='password')
        object = Feedback.objects.create(place = 'test', address='test', justification = 'test')
        response = self.client.post(reverse('uva_maps:submit_rating', kwargs={'feedback_id': object.id}), {'rating': 3})
        self.assertContains(response, '"newAverage": 3.0')

    def test_update_rating(self):
        self.client.login(username='test', password='password')
        object = Feedback.objects.create(place = 'test', address='test', justification = 'test')
        response = self.client.post(reverse('uva_maps:submit_rating', kwargs={'feedback_id': object.id}), {'rating': 3})
        response2 = self.client.get(reverse('uva_maps:get_updated_rating', kwargs={'feedback_id': object.id}))
        self.assertContains(response2, '3')        

