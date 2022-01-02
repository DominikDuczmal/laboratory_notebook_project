from django.test import TestCase, Client
from .models import User, Analyst, Supervisor, Task
from django.db.utils import IntegrityError, DataError
from django.utils import timezone


class AnalystTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='janekowal', password='pass1')
        User.objects.create(username='user_2', password='pass2')

        user_1 = User.objects.get(username='janekowal')

        Analyst.objects.create(
            first_name='Jan',
            last_name='Kowalski',
            email='jan.kowalski@gmail.com',
            laboratory=['1'],
            user=user_1,
        )

    def test_analyst_name(self):
        analyst = Analyst.objects.get(first_name='Jan', last_name='Kowalski')
        self.assertEqual(analyst.name, 'Jan Kowalski')

    def test_analyst_does_not_exist(self):
        with self.assertRaises(Analyst.DoesNotExist):
            Analyst.objects.get(first_name='Roman', last_name='Kowalski')

    def test_analyst_user_pk(self):
        user_1 = User.objects.get(username='janekowal')

        with self.assertRaises(IntegrityError):
            Analyst.objects.create(
                first_name='Jan_sobowtór',
                last_name='Kowalski_sobowtór',
                email='',
                laboratory=['1'],
                user=user_1,
            )

    def test_analyst_laboratory_array(self):
        user_2 = User.objects.get(username='user_2')
        with self.assertRaises(DataError):
            Analyst.objects.create(
                first_name='name_2',
                last_name='surname_2',
                email='',
                laboratory='1',
                user=user_2,
            )


class SupervisorTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='user_1', password='pass1')
        user_1 = User.objects.get(username='user_1')

        Supervisor.objects.create(
            first_name='Jan',
            last_name='Kowalski',
            email='jan.kowalski@gmail.com',
            laboratory=['1'],
            user=user_1,
        )

    def test_supervisor_is_supervisor(self):
        supervisor = Supervisor.objects.get(last_name='Kowalski')
        self.assertTrue(supervisor.is_supervisor)

    def test_supervisor_str(self):
        supervisor = Supervisor.objects.get(last_name='Kowalski')
        self.assertEqual(supervisor.__str__(), "Jan Kowalski - chief of  Organic Department")


class TaskTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='user_1', password='pass1')
        user_1 = User.objects.get(username='user_1')

        Analyst.objects.create(
            first_name='Jan',
            last_name='Kowalski',
            email='jan.kowalski@gmail.com',
            laboratory=['1'],
            user=user_1,
        )
        analyst = Analyst.objects.get(last_name="Kowalski")

        Task.objects.create(
            subject='My own subject',
            content="My own content",
            analyst_id=analyst
        )

    def test_task_str(self):
        task = Task.objects.get(subject='My own subject')
        self.assertEqual(task.__str__(), "My own subject")

    def test_task_date_sent(self):
        task = Task.objects.get(subject='My own subject')
        self.assertAlmostEqual(task.date_sent, timezone.now(), delta=timezone.timedelta(1))


class ClientTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_client_login(self):
        response = self.client.post('/login/', {'username': 'user_123', 'password': 'abc_123'})
        self.assertEqual(response.status_code, 200)

    def test_client_signup(self):
        response = self.client.post('/signup/', {
            'username': 'user_123',
            'password1': 'abc_123',
            'password2': 'abc_123'
        })
        self.assertEqual(response.status_code, 302)

    def test_client_signup_different_passwords(self):
        response = self.client.post('/signup/', {
            'username': 'user_123',
            'password1': 'abc_123',
            'password2': 'different'
        })
        self.assertEqual(response.context['error'], 'Passwords did not match')
        self.assertEqual(response.status_code, 200)

    def test_client_home_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_client_not_logged(self):
        views = [
            'get_analyst_form',
            'superior_overview',
            'create_task',
            'view_current_tasks',
            'view_completed_tasks',
            'view_task',
            'complete_task',
            'delete_task'
        ]

        for view in views:
            response = self.client.get(view)
            self.assertEqual(response.status_code, 404)

    def test_client_logged(self):
        user = User.objects.create(username='user_0')
        user.set_password('pass_0')
        user.save()

        logged_in = self.client.login(username='user_0', password='pass_0')

        self.assertTrue(logged_in)
