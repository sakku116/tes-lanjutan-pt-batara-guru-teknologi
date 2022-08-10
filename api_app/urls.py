from django.urls import path
from . import views

app_name = "api"

'''
urlpatterns = [
    path('register', views.register, name="register"),
    path('url-statistics/<int:id_url>', views.urlStatistics, name="url-statistics"),
]
'''
urlpatterns = [
    path('register', views.register, name="register"),
    path('login', views.logins, name="login"),
    path('short-url', views.shortUrl, name="short-url"),
    path('list-url', views.listUrl, name="list-url"),
    path('logout', views.logout_view, name="logout"),
    path('edit-url/<int:id_url>', views.editUrl, name="edit-url"),
    path('delete-url/<int:id_url>', views.deleteUrl, name="delete-url"),
    path('<str:url>', views.openShortedUrl)
]