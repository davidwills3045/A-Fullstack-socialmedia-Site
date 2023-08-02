from django.db import models
from django.contrib.auth import get_user_model
# from social_book.social_book.settings import DEFAULT_IMAGE_URL as default_image
user = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimage = models.ImageField(upload_to='profile_images',default="blank-profile-picture.png")
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
