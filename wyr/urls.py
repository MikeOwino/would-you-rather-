from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name="index"),
  path('login/', views.login_view, name="login"),
  path('logout/', views.logout_view, name="logout"),
  path("register/", views.register, name="register"),
  path("create/", views.create, name="create"),
  path("@<str:username>/", views.profile),
  path("api/<str:category>/<str:action>", views.api, name="api"),
  path("all/", views.all, name="all"),
  path("all/<int:q>", views.questions),
  path('moderate/<str:function>/', views.moderate, name="mod")
]