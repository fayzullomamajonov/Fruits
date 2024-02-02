from django.urls import path
from .views import *

urlpatterns = [
    path("home/", homepage_view, name="home"),
    path("fruits/list/", FruitsView.as_view(), name="fruits"),
    path("fruits/fruit/<int:pk>/", FruitView.as_view(), name="fruit"),
    path("add/fruit/", AddFruitView.as_view(), name="add_fruit"),
    path("fruits/update/<int:pk>/", UpdateFruitView.as_view(), name="update_fruit"),
    path("fruits/delete/<int:pk>/", DeleteFruitView.as_view(), name="delete_fruit"),
    path('fruits/add_comment/<int:pk>/', AddCommentView.as_view(), name='add_comment'),
    path("fruits/delete/comment/<int:pk>/", DeleteCommentView.as_view(), name="delete_comment"),
    path("fruits/update/comment/<int:pk>/", UpdateCommentView.as_view(), name="update_comment"),


]
