from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Expense(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.IntegerField("Amount")
    category=models.CharField(("Category"), max_length=50)
    date=models.DateField("Date")
    description=models.TextField(("Description"), max_length=200)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.category}"


class Income(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.IntegerField("Amount")
    source=models.CharField(("Source"), max_length=50)
    date=models.DateField("Date")
    
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.source}"
    
class Budget(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    amount=models.IntegerField(default=70000)
    savings_rate = models.FloatField(default=20)
    saving_goal = models.FloatField(default=50000)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount}"