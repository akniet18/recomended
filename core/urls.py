from django.urls import path, include

urlpatterns = [
    path('users/', include('users.urls')),
    path('reviews/', include('review.urls')),
    path('uploads/', include('uploads.urls')),
]