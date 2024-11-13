from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="materials"
    )
    code = models.CharField(max_length=50, unique=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
