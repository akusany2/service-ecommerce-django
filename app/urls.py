from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('editor', views.editor, name='editor'),
    path('editor/new-service', views.newService, name='new_service'),
    path('editor/edit-service/<int:index>', views.editService, name='edit_service'),
    path('editor/delete-service/<int:index>', views.deletService, name='delete_service'),
    path('clients', views.clients, name='clients'),

    path('client-order/<int:id>', views.clientPublic, name='clients-public'),
    
]
