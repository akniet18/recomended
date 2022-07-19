from django.db import models


class ProfessionalArea(models.Model):
    title = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class ActivityField(models.Model):
    title = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    professional_area = models.ForeignKey(ProfessionalArea, on_delete=models.CASCADE, related_name='professional_area')

    def __str__(self):
        return self.title

