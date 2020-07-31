from rest_framework import serializers
from .models import Practitioner, Patient, CholesterolPractitioner, CholesterolPatient, BloodPressurePractitioner, BloodPressurePatient, SmokerPractitioner, SmokerPatient

class PractitionerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Practitioner
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Patient
        fields =    '__all__'

class CholesterolPractitionerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CholesterolPractitioner
        fields = '__all__'

class CholesterolPatientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CholesterolPatient
        fields =    '__all__'

class BloodPressurePractitionerSerializer(serializers.ModelSerializer):

    class Meta:
        model = BloodPressurePractitioner
        fields = '__all__'

class BloodPressurePatientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BloodPressurePatient
        fields =    '__all__'

class SmokerPractitionerSerializer(serializers.ModelSerializer):

    class Meta:
        model = SmokerPractitioner
        fields = '__all__'

class SmokerPatientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SmokerPatient
        fields =    '__all__'
