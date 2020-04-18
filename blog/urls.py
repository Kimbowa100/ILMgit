from django.urls import path, include
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    OrderSummaryView,
    add_post_to_cart,
    #add_demo_to_cart,
    #add_template_to_cart,
    remove_post_from_cart,
    remove_single_post_from_cart,
    add_post_to_cart_without_redirect,
    #TemplateDetailView
    CheckoutView,
    PaymentView,
    all_stuff,
    FreestuffDetailsView,
    GenreListView,
    SongsByGenreListView,
    #ArtistListView,
   # ArtistDetailView,
    
    
    SongUploadView,
    FreestuffDetailView,
    FreestuffDeleteView,
    FreestuffUpdateView,
    UgandanListView,
    UgandanDetailView,
    InternationalListView,
    InternationalDetailView,
    FreestuffListView,
    PostList,
    
    
)
from . import views


urlpatterns = [
    path('blog/', views.PostList.as_view(), name='home'),
    path("<slug:slug>", views.post_detail, name="post_detail"),
    
    
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('freestuff/<int:pk>/update/',FreestuffUpdateView.as_view(), name='freestuff-update'),
    path('freestuff/<int:pk>/delete/', FreestuffDeleteView.as_view(), name='freestuff-delete'),
    
    
    
    path('ugandan-music/', UgandanListView.as_view(), name='ugandan-music'),
    path('ugandan-detail/<int:pk>/', UgandanDetailView.as_view(), name='ugandan-detail'),
    
    path('international-music/', InternationalListView.as_view(), name='international-music'),
    path('international-detail/<slug>/', InternationalDetailView.as_view(), name='international-detail'),
    path('freelist/', FreestuffListView.as_view(), name='freelist'),
    path('top_100/', views.top_100, name='top_100'),
    path('freestuffpost-detail/<int:pk>/', FreestuffDetailView.as_view(), name='freestuffpost-detail'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
 
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    #path('add-demo-to-cart/<slug>/', add_demo_to_cart, name="add-demo-to-cart"),
    path('add-post-to-cart/<int:pk>/', add_post_to_cart, name="add-post-to-cart"),
    #path('add-template-to-cart/<int:pk>/', add_template_to_cart, name="add-template-to-cart"),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('remove-post-from-cart/<int:pk>/', remove_post_from_cart, name='remove-post-from-cart'),
    
    path('remove-single-post-from-cart/<int:pk>/', remove_single_post_from_cart, name='remove-single-post-from-cart'),
    path('add-post-to-cart-without-redirect/<int:pk>/', add_post_to_cart_without_redirect, name='add-post-to-cart-without-redirect'),
    
    path('media/Files/<int:pk>',PostDeleteView.as_view(),name='post-delete' ),
    path('search/',views.search,name='search' ),
    path('about/', views.about, name='blog-about'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('payment/<payment_option>', PaymentView.as_view(), name='payment'),
    path('all-stuff/', views.all_stuff, name='all-stuff'),
    path('<slug:audio_id>', FreestuffDetailsView.as_view(), name='upload-details'),
    path('genres', GenreListView.as_view(), name='genres'),
    path('genres/<int:pk>', SongsByGenreListView.as_view(), name='songs-by-genre'),
    #path('artists/', ArtistListView.as_view(), name='artists'),
    #path('artists/<int:pk>', ArtistDetailView.as_view(), name='artist-details'),
    path('songs/', include([
        #path('make-favorite', favoriteunfavorite, name='song-favorite'),
        path('upload', SongUploadView.as_view(), name='upload'),
        path('<slug:audio_id>', FreestuffDetailsView.as_view(), name='upload-details'),
    ])),
    
    
    
    
]
