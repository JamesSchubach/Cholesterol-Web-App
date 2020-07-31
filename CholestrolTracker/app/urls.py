from django.urls import path, include, re_path
from django.views.generic import TemplateView
from . import viewsets
from .viewsets import PractitionerViewSet, PatientViewSet, CholesterolPractitionerViewSet, CholesterolPatientViewSet, BloodPressurePractitionerViewSet, BloodPressurePatientViewSet, SmokerPractitionerViewSet, SmokerPatientViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('practitioner', PractitionerViewSet, basename = 'practitioner')
router.register('patient', PatientViewSet, basename = 'patient')
router.register('cholesterolpractitioner', CholesterolPractitionerViewSet, basename = 'cholesterolpractitioner')
router.register('cholesterolpatient', CholesterolPatientViewSet, basename = 'cholesterolpatient')
router.register('bloodpressurepractitioner', BloodPressurePractitionerViewSet, basename = 'bloodpressurepractitioner')
router.register('bloodpressurepatient', BloodPressurePatientViewSet, basename = 'bloodpressurepatient')
router.register('smokerpractitioner', SmokerPractitionerViewSet, basename = 'smokerpractitioner')
router.register('smokerpatient', SmokerPatientViewSet, basename = 'smokerpatient')

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('api/', include(router.urls)),
    re_path(r'^(?P<path>.*)/$', TemplateView.as_view(template_name='index.html'))
]

