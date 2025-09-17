from django.urls import path
from .views import PneumoniaTestView, BrainTumorTestView

urlpatterns = [
    path("ml/pneumonia/", PneumoniaTestView.as_view(), name="pneumonia-test"),
    path("ml/braintumor/", BrainTumorTestView.as_view(), name="brian-tumor"),
] 