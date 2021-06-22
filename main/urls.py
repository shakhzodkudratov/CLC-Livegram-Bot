from django.urls import path

from main.views import MasterView, SlaveView

urlpatterns = [
    path('', MasterView.as_view()),
    path('<uuid:id>/', SlaveView.as_view()),
]
