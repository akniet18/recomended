from django.db import models
from uploads.utils import upload_file_path
from review.models import Review, Answer
from django.conf import settings
from users.models import User

class Upload(models.Model):
    name = models.CharField(max_length=1024, blank=True, null=True)
    file = models.FileField(upload_to=upload_file_path, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.SET_NULL, related_name='review_proof_docs', null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, related_name='answer_proof_docs', null=True, blank=True)
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE
    # )

    class Meta:
        ordering = ('uploaded_at',)
        verbose_name = 'Uploaded File'
        verbose_name_plural = 'Uploaded Files'

    def __str__(self):
        return f'{self.name} uploaded file'

    def save(self, *args, **kwargs):
        if self.review:
            if self.file:
                # self.review.moderated = False
                # self.review.moderator = User.objects.filter(role=User.ROLE_MODERATOR)[0]
                self.review.save()
        super(Upload, self).save(*args, **kwargs)

