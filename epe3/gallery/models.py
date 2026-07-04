from django.db import models
from django.contrib.auth.models import User

class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=150)
    painting_title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.painting_title} - {self.client_name}"
