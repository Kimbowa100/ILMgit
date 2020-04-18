from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django_countries.fields import CountryField
from blog.models import Share




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    studio = models.CharField(max_length=300)
    awards = models.CharField(max_length=400, blank=True)
    joined_on = models.DateTimeField(auto_now=True, null=True)
    contacts = models.IntegerField(default=1)
    email = models.CharField(max_length=50)
    country = CountryField(blank_label='(select country)')
    
    hit1 = models.CharField(max_length=50, blank=True)
    hit2 = models.CharField(max_length=50, blank= True)
    hit3 = models.CharField(max_length=50, blank= True)
    
    experience = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user.username} Profile'


    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

   
class CommentForm(models.Model):
      share = models.ForeignKey(Share, on_delete=models.DO_NOTHING)
      user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
      
     
      comment = models.TextField()
      
        
    
    
    
   
    
    
    
    