from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os
from django.conf import settings
from django_countries.fields import CountryField

from django.template.defaultfilters import slugify
import math
from time import strftime, gmtime
#from utils.song_utils import generate_file_name
from django.template.defaultfilters import slugify

from PIL import Image

CATEGORY_CHOICES = (
    
    ('Rnb', 'Rnb'),
    ('Pop', 'Pop'),
    ('Danncehall', 'Danncehall'),
    ('Afrobeat', 'Afrobeat'),
    ('Regae', 'Regae'),
    ('Afropop', 'Afropop'),
    
)
TYPE_CHOICES = (
    ('Beat', 'Beat'),
    ('Violin Piece', 'Violin Piece'),
    ('Guitar Piece', 'Guitar Piece'),
    ('Piano piece', 'Piano piece'),
    ('Vocal piece', 'Vocal piece'),
    ('African piece', 'African piece'),
    ('Trumpet Piece', 'Trumpet Piece'),
    ('Saxaphone Piec', 'Saxaphone Piece'),
    
)

class Genre(models.Model):
    name = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to="genres", default="default.jpeg")
    def __str__(self):
        return self.name
    
    
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    free_stuff = models.ForeignKey('Freestuff', on_delete=models.CASCADE)
    
class Freestuff(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_id = models.TextField()
    title = models.CharField(max_length=200, verbose_name="Song name")
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="thumbnails", blank=False)
    song = models.FileField(upload_to='Files')
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    #artists = models.ManyToManyField(Artist, related_name='songs')
    type = models.CharField(max_length=10)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(verbose_name='Created At', default=timezone.now)
    type_choice = models.CharField(choices=TYPE_CHOICES, max_length=20)
    country = CountryField(blank_label='(select country)')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('freestuffpost-detail', kwargs={'pk': self.pk})
    
    
class Artist(models.Model):
    name = models.CharField(max_length=200)
    artist_image = models.ImageField(upload_to='artist')
    
    def __str__(self):
        return self.name
 


    
                      
class UgandanMusic(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.DO_NOTHING)
    slug = models.SlugField()
    title = models.CharField(max_length=200, verbose_name="Song name")
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="thumbnails", blank=False)
    song = models.FileField(upload_to='Files')
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    #artists = models.ManyToManyField(Artist, related_name='songs')
    type = models.CharField(max_length=10)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(verbose_name='Created At', default=timezone.now)
    type_choice = models.CharField(choices=TYPE_CHOICES, max_length=20)
    country = CountryField(blank_label='(select country)')
    top_100 = models.BooleanField(default=False)
    def get_absolute_url(self):
        return reverse('ugandan-detail', kwargs={'pk': self.pk})
    def __str__(self):
        return self.title
                       
        
class InternationalMusic(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.DO_NOTHING, related_name='songs')
    slug = models.SlugField()
    title = models.CharField(max_length=200, verbose_name="Song name")
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="thumbnails", blank=False)
    song = models.FileField(upload_to='Files')
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    #artists = models.ManyToManyField(Artist, related_name='songs')
    type = models.CharField(max_length=10)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(verbose_name='Created At', default=timezone.now)
    type_choice = models.CharField(choices=TYPE_CHOICES, max_length=20)
    country = CountryField(blank_label='(select country)')
    top_100 = models.BooleanField(default=False)
    def get_absolute_url(self):
        return reverse('international-detail', kwargs={'slug': self.slug}
                       )
    def __str__(self):
        return self.title
         
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(null=True,blank=True,upload_to='Files')
    content = models.CharField(max_length=40)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category_choice = models.CharField(choices=CATEGORY_CHOICES, max_length=20, blank=True)
    type_choice = models.CharField(choices=TYPE_CHOICES, max_length=20, blank=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    made_with = models.CharField(max_length=50)
    date_posted = models.DateTimeField(default=timezone.now, blank=True)
    template = models.FileField(upload_to='products/',blank=True )
    demo = models.FileField(upload_to='products/', blank=True)
    Signature_beat = models.FileField(upload_to='products/', blank=True)
    plugins = models.CharField(max_length=100)
    Your_country = CountryField(blank_label='(select country)')
   
    
    
    
    
    def __str__(self):
        return self.title
    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk}
                       )
    def get_add_post_to_cart_url(self):
        return reverse("add-post-to-cart", kwargs={
            'pk': self.pk
        })
    def get_remove_post_from_cart_url(self):
        return reverse("remove-post-from-cart", kwargs={
            'pk': self.pk
        })
    def get_add_post_to_cart_without_redirect_url(self):
        return reverse("add-post-to-cart-without-redirect", kwargs={
            'pk': self.pk
        })    
    


class OrderPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_ordered = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file_quantity = models.IntegerField(default=1)
    
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    
class OrderP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posts = models.ManyToManyField(OrderPost)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    file_ordered = models.BooleanField(default=False)
    demo_ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True)
    
    def get_total(self):
        total = 0
        for order_post in self.posts.all():
            total += order_post.post.price
        return total
class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip =  models.CharField(max_length=100)
class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True )
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    

  
    
class ShareCategory(models.Model):
    
    title = models.CharField(max_length=400)
    share_image = models.ImageField(upload_to='share')
    preview_text = models.CharField(max_length=500)
class AboutAuthor(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='author')





"""class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

def get_topbanner_filename(instance, filename):
    title = instance.title
    slug = slugify(title)
    return "document/banner/{}/{}".format(slug, filename)
"""
STATUS = (
    (0,"Draft"),
    (1,"Publish")
) 
class Share(models.Model):
    share_category = models.ForeignKey(ShareCategory, on_delete=models.DO_NOTHING, null=True, blank=True )
    about_author = models.ManyToManyField(AboutAuthor)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, related_name='blog_posts')
    title = models.TextField()
    sub_title = models.TextField(blank=True)
    text = models.TextField()
    
    sub_title1 = models.TextField(blank=True)
    sub_title2 = models.TextField(blank=True)
    sub_title3 = models.TextField(blank=True)
    sub_title4 = models.TextField(blank=True)
    sub_title5 = models.TextField(blank=True)
    sub_title6 = models.TextField(blank=True)
    sub_title7 = models.TextField(blank=True)
    sub_title8 = models.TextField(blank=True)
    sub_title9 = models.TextField(blank=True)
    sub_title10 = models.TextField(blank=True)
    description = models.TextField(blank=True)
    description1 = models.TextField(blank=True)
    description2 = models.TextField(blank=True)
    description3 = models.TextField(blank=True)
    description4 = models.TextField(blank=True)
    description5 = models.TextField(blank=True)
    description6 = models.TextField(blank=True)
    description7 = models.TextField(blank=True)
    description8 = models.TextField(blank=True)
    description9 = models.TextField(blank=True)
    description10 = models.TextField(blank=True)
    description11= models.TextField(blank=True)
    description12= models.TextField(blank=True)
    description13= models.TextField(blank=True)
    description14= models.TextField(blank=True)
    description15= models.TextField(blank=True)
    image = models.ImageField(upload_to='sharepost', blank=True)
    image1 = models.ImageField(upload_to='sharepost', blank=True)
    image2 = models.ImageField(upload_to='sharepost', blank=True)
    image3 = models.ImageField(upload_to='sharepost', blank=True)
    image4= models.ImageField(upload_to='sharepost', blank=True)
    image5= models.ImageField(upload_to='sharepost', blank=True)
    image6= models.ImageField(upload_to='sharepost', blank=True)
    image7= models.ImageField(upload_to='sharepost', blank=True)
    image8= models.ImageField(upload_to='sharepost', blank=True)
    image9= models.ImageField(upload_to='sharepost', blank=True)
    image10= models.ImageField(upload_to='sharepost', blank=True)
    image11 = models.ImageField(upload_to='sharepost', blank=True)
    image12 = models.ImageField(upload_to='sharepost', blank=True)
    image13 = models.ImageField(upload_to='sharepost', blank=True)
    image14 = models.ImageField(upload_to='sharepost', blank=True)
    image15 = models.ImageField(upload_to='sharepost', blank=True)
    image16 = models.ImageField(upload_to='sharepost', blank=True)
    image17 = models.ImageField(upload_to='sharepost', blank=True)
    image18 = models.ImageField(upload_to='sharepost', blank=True)
    image19 = models.ImageField(upload_to='sharepost', blank=True)
    pdf = models.FileField(upload_to='sharepostpdf', blank=True)
    pdf1 = models.FileField(upload_to='sharepostpdf', blank=True)
    pdf2 = models.FileField(upload_to='sharepostpdf', blank=True)
    pdf3 = models.FileField(upload_to='sharepostpdf', blank=True)
    
    audio1 = models.FileField(upload_to='sharepostaudio', blank=True)
    audio2 = models.FileField(upload_to='sharepostaudio', blank=True)
    audio3 = models.FileField(upload_to='sharepostaudio', blank=True)
    audio4 = models.FileField(upload_to='sharepostaudio', blank=True)
    video1 = models.FileField(upload_to='sharepostvideo', blank=True)
    video2 = models.FileField(upload_to='sharepostvideo', blank=True)
    video3 = models.FileField(upload_to='sharepostvideo', blank=True)
    video4 = models.FileField(upload_to='sharepostvideo', blank=True)
    
    star = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    slug = models.SlugField(max_length=200, unique=True)
    #topbanner =  models.ImageField(upload_to=get_topbanner_filename, null=True, blank=True)
    #category  = models.ForeignKey(Hashtag,  on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('postdetail', args=[str(self.id)])


    class Meta:
        ordering = ['-created_on']


class Comment(models.Model):
    post = models.ForeignKey(Share,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)