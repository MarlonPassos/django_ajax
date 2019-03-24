from django.urls import path, include
from . import views 



urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/update/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('books/export/csv/', views.export_users_csv, name='export_users_csv'),
    path('books/export/xls/', views.export_users_xls, name='export_users_xls'),
]
