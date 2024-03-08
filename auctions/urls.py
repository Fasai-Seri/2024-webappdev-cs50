from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_listing', views.create_listing, name='create_listing'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('listing_page/<int:id>', views.listing_page, name='listing_page'),
    path('category', views.all_category, name='all_category'),
    path('category/<str:category_name>', views.listing_by_category, name='listing_by_category'),
    path('closed_listing', views.closed_listing, name='closed_listing')
]
