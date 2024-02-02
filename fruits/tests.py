from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from .forms import FruitsForm,FruitUpdateForm
from fruits.models import FruitsModel  

class AddFruitViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='TestPass123'
        )
        self.client.login(username='testuser', password='TestPass123')
        self.add_fruit_url = reverse('add_fruit')  

    def test_add_fruit_view_get(self):
        response = self.client.get(self.add_fruit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fruits/add_fruit.html')
        self.assertIsInstance(response.context['form'], FruitsForm)

    def test_add_fruit_view_post_valid_data(self):
        data = {
            'name': 'Apple',
            'price': 2.5,
            'short_info': 'A delicious fruit',
            'fruit_image': SimpleUploadedFile("apple.jpg", b"file_content", content_type="image/jpeg"),
        }

        response = self.client.post(self.add_fruit_url, data, follow=True)

        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'fruits/fruits.html')

        self.assertTrue(FruitsModel.objects.filter(name='Apple').exists())

class UpdateFruitViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='TestPass123'
        )
        self.client.login(username='testuser', password='TestPass123')
        self.fruit = FruitsModel.objects.create(
            name='Test Fruit',
            price=3.0,
            short_info='A delicious test fruit',
        )
        self.update_fruit_url = reverse('update_fruit', args=[self.fruit.id]) 

    def test_update_fruit_view_get(self):
        response = self.client.get(self.update_fruit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fruits/update_fruit.html')
        self.assertIsInstance(response.context['form'], FruitUpdateForm)
        self.assertEqual(response.context['fruit'], self.fruit)

    def test_update_fruit_view_post_valid_data(self):
        updated_name = 'Updated Fruit'
        updated_price = 4.0
        updated_short_info = 'An even more delicious updated fruit'
        updated_image = SimpleUploadedFile("updated_fruit.jpg", b"file_content", content_type="image/jpeg")

        data = {
            'name': updated_name,
            'price': updated_price,
            'short_info': updated_short_info,
            'fruit_image': updated_image,
        }

        response = self.client.post(self.update_fruit_url, data, follow=True)

        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'fruits/fruits.html') 

        updated_fruit = FruitsModel.objects.get(id=self.fruit.id)
        self.assertEqual(updated_fruit.name, updated_name)
        self.assertEqual(updated_fruit.price, updated_price)
        self.assertEqual(updated_fruit.short_info, updated_short_info)
        self.assertEqual(updated_fruit.fruit_image.name, 'media/' + updated_image.name) 

class DeleteFruitViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='TestPass123'
        )
        self.client.login(username='testuser', password='TestPass123')
        self.fruit = FruitsModel.objects.create(
            name='Test Fruit',
            price=3.0,
            short_info='A delicious test fruit',
        )
        self.delete_fruit_url = reverse('delete_fruit', args=[self.fruit.id])  

    def test_delete_fruit_view_get(self):
        response = self.client.get(self.delete_fruit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fruits/delete_fruit.html')
        self.assertEqual(response.context['fruit'], self.fruit)

    def test_delete_fruit_view_post(self):
        response = self.client.post(self.delete_fruit_url, follow=True)

        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'fruits/fruits.html') 

        self.assertFalse(FruitsModel.objects.filter(id=self.fruit.id).exists())