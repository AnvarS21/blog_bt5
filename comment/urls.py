from django.urls import path
from comment import views


urlpatterns = [
    path('', views.CommentCreateViews.as_view()),
    path('info/', views.UserCommentsView.as_view()),
    path('<int:pk>/', views.CommentDetailView.as_view()),
]