from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.utils.timezone import now

# Tee choice
TEES_CHOICES = [
    ('red', 'Red'), 
    ('yellow', 'Yellow'), 
    ('white', 'White'),
]

# Par choice
PAR_CHOICES = [
    (3, '3'), 
    (4, '4'), 
    (5, '5'),
]

# New model for round entry
class RoundModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rounds')
    date = models.DateField(default=now)
    course_name = models.CharField(max_length=50)
    tees = models.CharField(max_length=6, choices=TEES_CHOICES, default='yellow')

    def __str__(self):
        return f"{self.course_name} on {self.date}"


# Declare new model for holes
class HoleModel(models.Model):
    round = models.ForeignKey(RoundModel, on_delete=models.CASCADE, related_name='holes')
    hole_number = models.IntegerField(max_length=2)
    hole_par = models.IntegerField(choices=PAR_CHOICES, default='4')
    score = models.IntegerField(max_length=2)
    fairway = models.BooleanField()
    gir = models.BooleanField()
    putts = models.IntegerField()

    def __str__(self):
        return f"Hole {self.hole_number} - Score: {self.score}"

