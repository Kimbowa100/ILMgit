from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
    
)
from .models import Post, OrderPost,Artist, OrderP, ShareCategory, Share, AboutAuthor, BillingAddress, Payment, UserProfile, Freestuff, Genre, UgandanMusic, InternationalMusic, Comment
#, CommentReply, Document, UserImage, UserInfo, Hashtag
import operator
from django.urls import reverse_lazy
from django.contrib.staticfiles.views import serve

from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm, PaymentForm, FreestuffUploadForm, CommentForm
# CommentReplyForm, DocumentForm, BlogForm, UserImageForm, UserInfoForm
import stripe
from tinytag import TinyTag
from paypal.standard.forms import PayPalPaymentsForm

from decimal import Decimal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import formset_factory, modelformset_factory
from PIL import Image
from django import forms
#from simple_search import search_filter

stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc" 


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



def home(request):
    context = {
        'posts': Post.objects.all(),
        
    }
    return render(request, 'blog/home.html', context)

def search(request):
    template='blog/home.html'

    query=request.GET.get('q')

    result=Post.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query))
    paginate_by=2
    context={ 'posts':result }
    return render(request,template,context)


   


def getfile(request):
   return serve(request, 'File')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file','Signature_beat','template','demo','plugins','price','made_with',"type_choice","category_choice","Your_country"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = OrderP.objects.get(file_ordered=False)
        
            context = {
                'object': order
            }
        
            return render(self.request, 'blog/order_summary.html', context)
    
        except ObjectDoesNotExist:
            messages.warning(self.request, "you dont have an active order")
            return redirect('/')
    

def add_post_to_cart(request, pk):
    post = get_object_or_404(Post, pk=pk)
    order_post, created = OrderPost.objects.get_or_create(post=post, user=request.user, file_ordered=False,)
    order_qs = OrderP.objects.filter(user=request.user, file_ordered=False)
    
    if order_qs.exists():
        order=order_qs[0]
        if order.posts.filter(post__pk=post.pk).exists():
            order_post.file_quantity += 0
            order_post.save()
            messages.info(request, "the beat is already in download list.")
            
            return redirect("order-summary")
        else:
            messages.info(request, "this beat is added to download list")
            order.posts.add(order_post)
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = OrderP.objects.create(user=request.user, ordered_date=ordered_date )
        order.posts.add(order_post)
        messages.info(request, "This item was added to your cart.")        
        return redirect("order-summary")
def add_post_to_cart_without_redirect(request, pk):
    post = get_object_or_404(Post, pk=pk)
    order_post, created = OrderPost.objects.get_or_create(post=post, user=request.user, file_ordered=False,)
    order_qs = OrderP.objects.filter(user=request.user, file_ordered=False)
    
    if order_qs.exists():
        order=order_qs[0]
        if order.posts.filter(post__pk=post.pk).exists():
            order_post.file_quantity += 0
            order_post.save()
            messages.info(request, "the beat is already in download list.")
            
            return redirect("blog-home")
        else:
            messages.info(request, "this beat is added to download list")
            order.posts.add(order_post)
            return redirect("blog-home")
    else:
        ordered_date = timezone.now()
        order = OrderP.objects.create(user=request.user, ordered_date=ordered_date )
        order.posts.add(order_post)
        messages.info(request, "This item was added to your cart.")        
        return redirect("blog-home")


def remove_post_from_cart(request, pk):
    post = get_object_or_404(Post, pk=pk)
    order_qs = OrderP.objects.filter(
        user=request.user,
        file_ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.posts.filter(post__pk=post.pk).exists():
            order_post = OrderPost.objects.filter(
                post=post,
                user=request.user,
                file_ordered=False
            )[0]
            order.posts.remove(order_post)
            order_post.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("blog-home")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("blog-home")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("blog-home")
    
def remove_single_post_from_cart(request, pk):
    post = get_object_or_404(Post, pk=pk)
    order_qs = OrderP.objects.filter(
        user=request.user,
        file_ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.posts.filter(post__pk=post.pk).exists():
            order_post = OrderPost.objects.filter(
                post=post,
                user=request.user,
                file_ordered=False
            )[0]
            if order_post.file_quantity > 1:
                order_post.file_quantity -= 1
                order_post.save()
            else:
                order.posts.remove(order_post)
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("blog-home")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("blog-home")
class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'blog/checkout.html', context)
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = OrderP.objects.get(file_ordered=False)
            print(self.request.POST)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                payment_option = form.cleaned_data.get('payment_option')
                #same_billing_address = form.cleaned_data.get('same_billing_address')
                billing_address = BillingAddress(
                    user =self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    country = country,
                    zip = zip
                    )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect('process_payment')
            messages.warning(self.request, "Order Placed")
            return redirect('process_payment')
        
            
    
        except ObjectDoesNotExist:
            messages.warning(self.request, "you dont have an active order")
            return redirect('checkout')



def process_payment(request):
    file_ordered = request.session.get('file_ordered')
    order = get_object_or_404(OrderP, file_ordered=False)
    host = request.get_host()
 
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.get_total(),
        'item_name': 'OrderP {}'.format(order.billing_address.apartment_address),
        
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }
 
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'blog/process_payment.html', {'order': order, 'form': form})


@csrf_exempt
def payment_done(request):
    return render(request, 'blog/payment_done.html')
 
 
@csrf_exempt
def payment_canceled(request):
    return render(request, 'blog/payment_cancelled.html')     
class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'blog/payment.html') 
    
    def post(self, *args, **kwargs):
        order = OrderP.objects.get(user=self.request.user, file_ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)

            try:

                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        source=token
                    )

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()

                # assign the payment to the order

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()
                order.save()

                messages.success(self.request, "Your order was successful!")
                return redirect("/")

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")
             
        

def all_stuff(request):
    latest_songs=Freestuff.objects.all()[:6],


    context = {
        'artists':User.objects.all(),
        'genres': Genre.objects.all(),
        'latest_songs':Freestuff.objects.all(),
        
        'all_posts' : Post.objects.all(),
        
    }
    
    page = request.GET.get('page', 1)

    paginator = Paginator(latest_songs, 4)
    try:
        latest_songs = paginator.page(page)
    except PageNotAnInteger:
        latest_songs = paginator.page(1)
    except EmptyPage:
        latest_songs = paginator.page(paginator.num_pages)

    return render(request, "all_stuff.html", context)

class FreestuffListView(ListView):
    model = Freestuff
    template_name = 'blog/free_list.html'
    context_object_name = 'freelist'
    paginate_by = 20
    
class FreestuffDetailsView(DetailView):
    model = Freestuff
    template_name = 'songs/show.html'
    context_object_name = 'song'
    slug_field = 'audio_id'
    slug_url_kwarg = 'audio_id'
    
class UgandanListView(ListView):
    model = UgandanMusic
    template_name = 'general_music/ugandan_music.html'
    context_object_name = 'ugandan'
    paginate_by = 2
    
class UgandanDetailView(DetailView):
    model = UgandanMusic
    template_name = 'general_music/show.html'
    context_object_name = 'ugandandetail'

    
    
class InternationalListView(ListView):
    model = InternationalMusic
    template_name = 'international_music/international_music.html'
    context_object_name = 'international'
    paginate_by = 2
    
class InternationalDetailView(DetailView):
    model = InternationalMusic
    template_name = 'international_music/show.html'
    context_object_name = 'internationaldetail'   

def top_100(request):
    top_international = InternationalMusic.objects.filter(top_100=True)
    top_ugandan = UgandanMusic.objects.filter(top_100=True)
    
    context = {
        'top_international': top_international,
        'top_ugandan': top_ugandan
    }
    return render(request, 'blog/top_songs.html', context)

    

class GenreListView(ListView):
    model = Genre
    template_name = 'genres/index.html'
    context_object_name = 'genres'
    
class SongsByGenreListView(DetailView):
    model = Genre
    template_name = 'genres/songs-by-genre.html'
    context_object_name = 'genre'
    paginate_by = 6
    def get_context_data(self, **kwargs):
        context = super(SongsByGenreListView, self).get_context_data(**kwargs)
        context['songs'] = self.get_object().freestuff_set.all
        return context   
"""class ArtistListView(ListView):
    model = Artist
    template_name = 'artists/index.html'
    context_object_name = 'artists'
    
class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'artists/show.html'
    context_object_name = 'artist'
    

    def get_context_data(self, **kwargs):
        context = super(ArtistDetailView, self).get_context_data(**kwargs)
        context['internationals'] = InternationalMusic.objects.all()
        context['ugandans'] = UgandanMusic.objects.all()
        return context  
"""   
     
class SongUploadView(LoginRequiredMixin, CreateView):
    model = Freestuff
    template_name = 'songs/create.html'
    fields = ["title","description","audio_id","type", "genre","thumbnail", "song","type_choice","country"]
    
    def get_context_data(self, **kwargs):
        context = super(SongUploadView, self).get_context_data(**kwargs)
        context['artists'] = User.objects.all()
        context['genres'] = Genre.objects.all()
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class SongloadView(CreateView):
    form_class = FreestuffUploadForm
    template_name = "songs/create.html"

    @method_decorator(login_required(login_url=reverse_lazy('upload')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SongUploadView, self).get_context_data(**kwargs)
        context['artists'] = Artist.objects.all()
        context['genres'] = Genre.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super(SongUploadView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=200)

    def form_valid(self, form):
        song = TinyTag.get(self.request.FILES['song'].file.name)
        #form.instance.audio_id = generate_key(15, 15)
        form.instance.user = self.request.user
        form.instance.playtime = song.duration
        form.instance.size = song.filesize
        artists = []
        for a in self.request.POST.getlist('artists[]'):
            try:
                artists.append(int(a))
            except:
                artist = Artist.objects.create(name=a)
                artists.append(artist)
        form.save()
        form.instance.artists.set(artists)
        form.save()
        data = {
            'status': True,
            'message': "Successfully submitted form data.",
            'redirect': reverse_lazy('core:upload-details', kwargs={'audio_id': form.instance.audio_id})
        }
        return JsonResponse(data)
    
    



class UserFreestuffListView(ListView):
    model = Freestuff
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class FreestuffDetailView(DetailView):
    model = Freestuff
    template_name = 'free_stuff/freestuff_detail.html'
    
class FreestuffUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Freestuff
    template_name = 'free_stuff/freestuff_form.html'
    fields = ['title', 'description', 'song']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        freestuff = self.get_object()
        if self.request.user == freestuff.author:
            return True
        return False


class FreestuffDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Freestuff
    success_url = '/'
    template_name = 'free_stuff/freestuff_confirm_delete.html'

    def test_func(self):
        freestuff = self.get_object()
        if self.request.user == freestuff.author:
            return True
        return False
    

class ShareCategoryList(ListView):
    model = ShareCategory
    template_name = 'share_ideas/share_category.html'
    context_object_name = 'sharecategory'
    
      
class ShareCategorybyShare(DetailView):
    model = ShareCategory
    template_name = 'share_ideas/share_page.html'
    context_object_name = 'shared'


    def get_context_data(self, **kwargs):
        context = super(ShareCategorybyShare, self).get_context_data(**kwargs)
        context['shares'] = self.get_object().share_set.all()
        return context  


class PostList(ListView):
    queryset = Share.objects.filter(status=1).order_by('-created_on')
    template_name = 'share/index.html'

def post_detail(request, slug):
    template_name = 'share/post_detail.html'
    post = get_object_or_404(Share, slug=slug)
    # i may have to change post to share
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
