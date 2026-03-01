from django.db import models


class Equipment(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=250)
    Image = models.FileField(upload_to='uploads/Equipments', blank=True)

    def __str__(self):
        return self.Name

