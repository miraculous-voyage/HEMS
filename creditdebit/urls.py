from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('give_take/<int:dash_id>', views.give_take, name='give_take'),
    path('tables',views.tables, name='tables'),
    path('reports',views.reports, name='reports'),    
    path('tables/datatable',views.datatable, name='datatable'),
    path('tables/datatable/<int:item_id>', views.datatable_detail, name='datatable_detail'),
    path('tables/usertable',views.usertable, name='usertable'),
    path('tables/datatable/add_to_datatable',views.add_to_datatable, name='add_to_datatable'),
    
]
