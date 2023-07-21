from django.db import models
from django.contrib.auth.models import User
import uuid


class Account(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=256, null=True, blank=True)
    first_name = models.CharField(max_length=256, null=True, blank=True)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to="images/profile_pictures",
                                        default="images/profile_pictures/default_profile.png",
                                        null=True,
                                        blank=True
                                        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = self.owner.email

        if not self.first_name:
            self.first_name = self.owner.first_name

        if not self.last_name:
            self.last_name = self.owner.last_name
        
        if not self.username:
            self.username = self.owner.username
        super().save(*args, **kwargs)

    def __str__(self):
        if self.first_name == "" or self.last_name == "":
            return self.username
        return f"{self.first_name} {self.last_name}"

    @property
    def profile_picture_url(self):
        if self.profile_picture:
            pass
        else:
            self.profile_picture = "images/profile_pictures/default_profile.png"
            self.save()

        return self.profile_picture


class ImageUploadTest(models.Model):
    image_field = models.ImageField(upload_to="images/test_image_folder")
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
