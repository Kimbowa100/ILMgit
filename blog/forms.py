from django import forms
from django_countries.fields import CountryField
from .models import Freestuff, Favorite, Share, Comment
# CommentReply,  Document, UserImage, UserInfo

from django.forms import ModelForm, ImageField, FileField
from PIL import Image
from django.core.files.images import get_image_dimensions
from django.core.files import File
#from simple_search import search_form_factory

PAYMENT_CHOICES = (
    ('M', 'Mtn MomoPay'),
    ('S', 'Stripe'),
    ('P', 'Paypal')
)

CATEGORY_CHOICES = (
    
    ('Rb', 'Rnb'),
    ('Pp', 'Pop'),
    ('Dh', 'Danncehall'),
    ('Ab', 'Afrobeat'),
    ('RA', 'Regae'),
    ('AP', 'Afropop'),
    
)
TYPE_CHOICES = (
    ('BI', 'Beat'),
    ('VI', 'Violin Piece'),
    ('GI', 'Guitar Piece'),
    ('PI', 'Piano piece'),
    ('VI', 'Vocal piece'),
    ('AI', 'African piece'),
    ('TI', 'Trumpet Piece'),
    ('SI', 'Saxaphone Piece'),
    
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField( max_length=50)
    apartment_address = forms.CharField( max_length=40, required=False)
    country = CountryField(blank_label='(select country)').formfield(
        required=False,
       )
    zip = forms.CharField()
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput())
class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)    

class FreestuffUploadForm(forms.ModelForm):
    category_choice = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True )
    type_choice = forms.ChoiceField(choices=TYPE_CHOICES, required=True )
    class Meta:
        model = Freestuff
        fields = ("title", "description", "type", "genre", "thumbnail", "song","category_choice","type_choice")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FreestuffUploadForm, self).__init__(*args, **kwargs)

    def clean_user(self):
        return self.user


class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ("post", "free_stuff")

    def clean_song(self):
       pass
   
"""
class BlogForm(ModelForm):
    class Meta:
        model = Share
        exclude = ('date', 'star', 'author',)

class DocumentForm(ModelForm):
    image = FileField(label='Image')
    class Meta:
        model = Document
        fields = ('image', )

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['message']

class CommentReplyForm(ModelForm):
    class Meta:
        model = CommentReply
        fields = ['message']
   
class UserImageForm(ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = UserImage
        fields = ('myimage','x', 'y', 'width', 'height')


    def save(self):
        photo = super(UserImageForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.myimage)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.myimage.path)

        return photo

class UserInfoForm(ModelForm):
    email = forms.EmailField()
    class Meta:
        model = UserInfo
        exclude = ('author', 'views')
        fields = ('displayname', 'designation', 'description', 'birthdate', 'email')
        fields = '__all__'
"""
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')     
