from rest_framework.authtoken.admin import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse


class UserTestCase(APITestCase):

    def setUp(self):
        # Создаем нового пользвователя в нашем приложении
        user = User.objects.create(username='new_user', email='new_user@gmail.com')
        user.set_password('A123123123')
        user.save()

    def test_user_api(self):
        # Логинимся нашим пользователем в системе
        url = reverse('api:login')
        data = {
            'username': 'new_user',
            'password': 'A123123123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Получаем токен для доступа к функциям администратора (например для создания новых опросов)
        token = response.data.get('token', 0)
        token_len = len(token)
        self.assertGreater(token_len, 0)

        # Создаем нового пользователя при помощи API
        url = reverse('api:users-list')
        data = {
            "username": "rob",
            "first_name": "Robert",
            "last_name": "Burns",
            "is_active": "true",
            "last_login": "null",
            "is_superuser": "false",
            "password": "S333333333"
        }
        response = self.client.post(url, data, format='json',  HTTP_AUTHORIZATION='Token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем что новый пользователь создан
        new_user_id = response.data['id']
        url = reverse('api:users-detail', args=[new_user_id])
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION='Token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем наличие несуществующего пользователя
        url = reverse('api:users-detail', args=[3])
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION='Token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Вносим изменения в данные созданного пользователя
        url = reverse('api:users-detail', args=[new_user_id])
        data = {
            "username": "rob1",
            "first_name": "Robert1",
            "last_name": "Burns1",
            "is_active": "true",
            "last_login": "null",
            "is_superuser": "false",
            "password": "S333333333zsdasd"
        }
        response = self.client.put(url, data, format='json',  HTTP_AUTHORIZATION='Token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Вносим частичные изменения в данные созданного пользователя
        data = {
            "is_active": "false",
            "password": "Sz21221dasd"
        }
        response = self.client.patch(url, data, format='json',  HTTP_AUTHORIZATION='Token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Удаляем пользователя из базы
        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION='Token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Пытаемся повторно удалить пользователя
        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION='Token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
