from django.db import models

# Create your models here.
class Data(models.Model):
    name = models.CharField(max_length=120)  # max_length = required
    DateOfBirth = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("products:product-detail", kwargs={"id": self.id})