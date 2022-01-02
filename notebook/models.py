from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

LABORATORIES = (
    ('1', "Organic"),
    ('2', 'Non Organic'),
    ('3', 'Research and development'),
    ('4', 'Quality Control')
)


class Analyst(models.Model):
    """Class implementing a Model for Laboratory Analysts.

    It stores a list of fields and behaviors of the Data.
    """

    first_name = models.CharField(max_length=25, verbose_name='Imię')
    last_name = models.CharField(max_length=80, verbose_name='Nazwisko')
    email = models.EmailField(null=True, blank=True, verbose_name='E-mail')
    laboratory = ArrayField(
        models.CharField(choices=LABORATORIES, max_length=1, verbose_name='Laboratorium')
    )

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.name


class Supervisor(Analyst):
    """Class implementing a Model for Laboratory Supervisors.

    It stores a list of fields and behaviors of the Data and is based on Analyst Model.
    """

    is_supervisor = models.BooleanField(default=True, verbose_name='Kierownik')

    def __str__(self):
        laboratory_name = LABORATORIES[int(self.laboratory[0]) - 1][1]
        return f'{self.name} - chief of  {laboratory_name} Department'


class Task(models.Model):
    """Class implementing a Model for Laboratory Tasks.

    It stores a list of fields and behaviors of the Data.
    """

    subject = models.CharField(max_length=254, verbose_name='Temat Analizy/Badania')
    content = models.TextField(verbose_name='Notatki z przeprowadzonego eksperymentu')
    analyst_id = models.ForeignKey(Analyst, on_delete=models.CASCADE, verbose_name='Analityk')
    photos = models.ImageField(upload_to='my_media', null=True, blank=True)
    date_sent = models.DateTimeField(auto_now_add=True, verbose_name='Data wysłania')
    date_completed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject
