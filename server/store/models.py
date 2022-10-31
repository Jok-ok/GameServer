from django.db import models

from users.models import User


# Create your models here.
class Store(models.Model):
    title = models.CharField(primary_key = True, max_length=255, unique=True)
    price = models.IntegerField()
    category = models.CharField(max_length=255)
    image = models.ImageField(upload_to = '')

    def __str__(self):
        return str(self.image)


class Inventory(models.Model):
    title = models.ForeignKey(Store, on_delete=models.CASCADE)
    nickname = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('title', 'nickname')