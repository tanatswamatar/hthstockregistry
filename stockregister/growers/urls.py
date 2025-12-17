from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('allocate/', views.allocate_stock, name='allocate_stock'),
    path('officer/<int:officer_id>/', views.officer_growers, name='officer_growers'),
    path('grower/<int:grower_id>/', views.grower_detail, name='grower_detail'),

    path('grower/<int:grower_id>/invoice/', views.generate_invoice_pdf, name='generate_invoice'),
    path('export/excel/', views.export_growers_excel, name='export_excel'),
    path('accounts/', include('django.contrib.auth.urls')),

]
