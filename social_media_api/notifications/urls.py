from django.urls import path
from .views import NotificationListView, NotificationMarkReadView, NotificationMarkAllReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications'),
    path('<int:pk>/read/', NotificationMarkReadView.as_view(), name='notification-read'),
    path('mark-all-read/', NotificationMarkAllReadView.as_view(), name='notifications-mark-all-read'),
]
