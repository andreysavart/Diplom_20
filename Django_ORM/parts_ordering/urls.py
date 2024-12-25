from django.urls import path

from . import views


urlpatterns = [
    path('bolts/', views.get_bolts, name='bolts'),
    path('bolt/create/', views.BoltCreateView.as_view(), name='bolt_create'),
    path('bolt/<int:pk>/', views.BoltDetailView.as_view(), name='bolt_detail'),
    path('bolt/<int:pk>/update', views.BoltUpdateView.as_view(), name='bolt_update'),
    path('nuts/', views.get_nuts, name='nuts'),
    path('nut/create/', views.NutCreateView.as_view(), name='nut_create'),
    path('nut/<int:pk>/', views.NutDetailView.as_view(), name='nut_detail'),
    path('nut/<int:pk>/update', views.NutUpdateView.as_view(), name='nut_update'),
    path('washers/', views.get_washers, name='washers'),
    path('washer/create/', views.WasherCreateView.as_view(), name='washer_create'),
    path('washer/<int:pk>/', views.WasherDetailView.as_view(), name='washer_detail'),
    path('washer/<int:pk>/update', views.WasherUpdateView.as_view(), name='washer_update'),
    path('bolt_joints/', views.get_bolt_joints, name='bolt_joints'),
    path('bolt_joint/create/', views.BoltJointCreateView.as_view(), name='bolt_joint_create'),
    path('bolt_joint/<int:pk>/', views.BoltJointDetailView.as_view(), name='bolt_joint_detail'),
    path('bolt_joint/<int:pk>/update', views.BoltJointUpdateView.as_view(), name='bolt_joint_update'),
    path('orders/', views.index, name='index'),
    path('order/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/<int:pk>/update', views.OrderUpdateView.as_view(), name='order_update'),
]
