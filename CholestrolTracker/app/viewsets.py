from .models import Practitioner, Patient, CholesterolPractitioner, CholesterolPatient, BloodPressurePractitioner, BloodPressurePatient, SmokerPractitioner, SmokerPatient
from .serializers import PractitionerSerializer, PatientSerializer, CholesterolPractitionerSerializer, CholesterolPatientSerializer, BloodPressurePatientSerializer, BloodPressurePractitionerSerializer, SmokerPractitionerSerializer, SmokerPatientSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import QueryDict
import json
import time
import requests

class PractitionerViewSet(viewsets.ModelViewSet):

    """
    Controller for Practitioner - gets and updates data in Practitioner Model
    Handles API requests from the front-end
    """

    # List of all practitioners in the database (Model)
    queryset = Practitioner.objects.all()
    practitioner_queryset = queryset
    # The class that serializes/deserializes data to/from front-end (handled by Django serializers)
    serializer_class = PractitionerSerializer
    # The specific lookup fields to view/filter practitioner objects by
    lookup_field = 'identifier'
    filter_fields = ('identifier',)

    def retrieve(self, request, identifier=None):

        """
        Based on an API GET request, this gets data for a particular practitioner in the database (queryset) using its identifier
        and returns a JSON response. If the practitioner can't be found, it checks if the identifier
        is valid (by checking the FHIR server), and then retrieves the practitioner's info from the FHIR
        server and returns it as a JSON response
        Called using root_url + '/practitioner/<identifier>/' 
        """

        practitioner_data = self.getPractitioner(identifier)
        if practitioner_data == False:
            return Response({'error': 'Invalid Practitioner Identifier'}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(practitioner_data)

    def partial_update(self, request, identifier = None):

        """
        Based on an API PATCH request, this partially updates a practitioner object with a given identifier
        Called using root_url + /practitioner/identifier/?<params>
        """

        data = request.query_params
        # updated_data = self.practitionerUpdated(data, identifier)

        # if updated_data == False:
        #     return Response({'error': 'Invalid query - details not valid'}, status = status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response(updated_data)

    def getPractitioner(self, identifier):
        
        """
            Gets a practitioner in the database or creates one using the FHIR server if it doesn't exist
            and returns a response with the practitioner's data
        """

        # Try to find the practitioner in the database using Practitioner Model object
        try:
            practitioner = Practitioner.objects.get(identifier = identifier)
        
        # If it doesn't exist, check to see if it's a valid identifier and then create one
        except:
            print(self.checkPractitionerIdentifier(identifier))
            if self.checkPractitionerIdentifier(identifier):
                practitioner = Practitioner(identifier = identifier)
                practitioner.save(request = 'get')
                practitioner = Practitioner.objects.get(identifier = identifier)
            # Or return an error if the identifier is invalid
            else:
                return False
        # Potential Speed-up
            # practitioner.savePatients()
            # patients = practitioner.fromJson()
        
        # Filter through all patients that the practitioner has seen to form a patients list
        patients = Patient.objects.filter(practitioner = practitioner.identifier)
        
        patient_list = []
        for patient in patients:
            patient_list.append(PatientSerializer(patient).data)

        # Return a response with all info of the Practitioner model + list of associated patients
        response = {
            'identifier': practitioner.identifier,
            # 'average_cholesterol': practitioner.average_cholesterol,
            # 'filter_cholesterol': practitioner.filter_cholesterol,
            # 'refresh_rate': practitioner.refresh_rate,
            'patients': patient_list
        }
        
        return response

    def practitionerUpdated(self, query_params, identifier):

        """
        Updates data for a practitioner object using query_params data
        """

        try:
            # Get the practitioner object by its identifier
            practitioner = Practitioner.objects.get(identifier = identifier)

            # Update the fields in the Model
            try:
                refresh_rate = query_params['refresh_rate']
                practitioner.refresh_rate = int(refresh_rate)
            except:
                print("break at refresh")
                pass

            try:
                filter_cholesterol = query_params['filter_cholesterol']
                practitioner.filter_cholesterol = int(filter_cholesterol)
                print("made it here")
                practitioner.getHighlighted()
            except:
                print('break')
                pass
            
            practitioner.save(request = 'patch')
            response = PractitionerSerializer(Practitioner.objects.get(identifier = identifier)).data
            return response
        except:
            return False

    def checkPractitionerIdentifier(self, identifier):

        """
        Checks to see if a practitioner identifier is valid according to the FHIR server
        """

        try: 
            # Check to see if there are any entries for the practitioner
            root_url = 'https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/'
            encounters_url = root_url + 'Encounter?_include=Encounter.participant.individual&_include=Encounter.patient&participant.identifier=http%3A%2F%2Fhl7.org%2Ffhir%2Fsid%2Fus-npi%7C{}'
            encounters_url = encounters_url.format(str(identifier))
            print(encounters_url)
            all_encounters_practitioner = requests.get(url=encounters_url).json()
            all_encounter_data=all_encounters_practitioner['entry']
            return True
        # If there are none, an exception will be returned
        except:
            return False

class PatientViewSet(viewsets.ModelViewSet):

    """
    Controller for Patient - gets and updates data in Patient Model
    Handles API requests from the front-end
    """

    # List of all patients in the database (Model)
    queryset = Patient.objects.all()
    patient_queryset = queryset
    # The class that serializes/deserializes data to/from front-end (handled by Django serializers)
    serializer_class = PatientSerializer
    # The specific lookup fields to view/filter patient objects by
    lookup_field = 'id'
    filter_fields = ('id',)

    def retrieve(self, request, id=None):

        """
        Based on an API GET request, this gets data for a particular patient in the database 
        (queryset) using its ID and returns a JSON response
        Called using root_url + '/patient/<id>/' 
        """

        patient_data = self.getPatient(id)
        return Response(patient_data)

    def partial_update(self, request, id=None):
        """
        Based on an API PATCH request, this partially updates a patient object with a given id
        Called using root_url + /patient/id/?<params>
        """

        data = request.query_params
        # updated_data = self.patientUpdated(data, id)

        # if updated_data == False:
        #     return Response({'error': 'Invalid query - details not valid'}, status = status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response(updated_data)

    def getPatient(self, id):

        """
        Gets a patient in the database if it already exists
        """

        try:
            patient = Patient.objects.get(id = id)
        # Otherwise return error
        except:
            return Response({'error': 'Invalid Patient ID'}, status = status.HTTP_400_BAD_REQUEST)

        response = PatientSerializer(patient).data
        return response
    
    def patientUpdated(self, query_params, id):

        """
        Updates a patient in the database based on query_params
        """

        try:
            # Get the parameters the API call wants to update
            patient = Patient.objects.get(id = id)

            # Update the parameters in the Model
            try:
                visible = query_params['visible']
                patient.visible = visible
                patient.practitioner.calculateAverageCholesterol()
                patient.practitioner.getHighlighted()
            except:
                print("Breaks")
                pass

            try:
                highlighted = query_params['highlighted']
                print(highlighted)
                patient.highlighted = highlighted
            except:
                pass
            
            patient.save()
            response = PatientSerializer(Patient.objects.get(id = id)).data
            return response
        except:
            response = False
            return response
        
class CholesterolPractitionerViewSet(PractitionerViewSet):
    """
    Controller for CholesterolPractitioner - gets and updates data in Cholesterol Practitioner Model
    Handles API requests from the front-end. This is the concrete implementation of the PractitionerViewSet
    """

    # List of all practitioners in the database (Model)
    queryset = CholesterolPractitioner.objects.all()
    practitioner_queryset = queryset
    # The class that serializes/deserializes data to/from front-end (handled by Django serializers)
    serializer_class = CholesterolPractitionerSerializer
    # The specific lookup fields to view/filter practitioner objects by
    lookup_field = 'identifier'
    filter_fields = ('original_practitioner',)

    def retrieve(self, request, identifier = None):
        """
        Based on an API GET request, this gets data for a particular CholestrolPractitioner in the database 
        (queryset) using its ID and returns a JSON response
        Called using root_url + '/cholesterolpractitioner/<id>/' 
        """
        try:
            original_practitioner = Practitioner.objects.get(identifier = identifier)
            try:
                chol_practitioner = CholesterolPractitioner.objects.get(original_practitioner = original_practitioner)
                # chol_practitioner.save(request = 'get')
            except:
                try:
                    chol_practitioner = CholesterolPractitioner(chol_prac_id = 0, original_practitioner = original_practitioner)
                except Exception as e:
                    print(e)
            chol_practitioner.save(request = 'get')
            chol_practitioner = CholesterolPractitioner.objects.get(original_practitioner = original_practitioner)
            response = CholesterolPractitionerSerializer(chol_practitioner).data
            print(response)
            response.update(PractitionerSerializer(original_practitioner).data)
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Practitioner not instantiated in Model yet'}, status = status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, identifier = None):
        """
        Based on an API PATCH request, this partially updates a practitioner object with a given id
        Called using root_url + /cholesterolpractitioner/id/?<params>
        """
        try:
            # Get the practitioner object by its identifier
            # original_prac = Practitioner.objects.get(identifier = identifier)
            # practitioner = CholesterolPractitioner.objects.get(original_practitioner = original_prac)

            # Update the fields in the Model
            try:
                refresh_rate = request.query_params['refresh_rate']
                self.refreshRateUpdated(refresh_rate, identifier)
            except:
                pass

            try:
                filter_cholesterol = request.query_params['filter_cholesterol']
                self.filterCholesterolUpdated(filter_cholesterol, identifier)
                #practitioner.getHighlighted()
            except:
                pass
            
            original_prac = Practitioner.objects.get(identifier = identifier)
            practitioner = CholesterolPractitioner.objects.get(original_practitioner = original_prac)
            practitioner.save(request = 'patch')
            response = CholesterolPractitionerSerializer(practitioner).data
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Invalid query - details not valid'}, status = status.HTTP_400_BAD_REQUEST)

    def filterCholesterolUpdated(self, filter_cholesterol, identifier):
        """
        Function that takes filter_cholesterol value and then saves that to the practitioner
        """
        original_prac = Practitioner.objects.get(identifier = identifier)
        practitioner = CholesterolPractitioner.objects.get(original_practitioner = original_prac)
        practitioner.filter_cholesterol = int(filter_cholesterol)
        practitioner.save(request='patch')

    def refreshRateUpdated(self, refresh_rate, identifier):
        """
        Function that takes refresh_rate value and then saves that to the practitioner
        """
        original_prac = Practitioner.objects.get(identifier = identifier)
        practitioner = CholesterolPractitioner.objects.get(original_practitioner = original_prac)
        practitioner.refresh_rate = int(refresh_rate)
        practitioner.save(request='patch')

class CholesterolPatientViewSet(PatientViewSet):
    """
    Controller for CholesterolPatient - gets and updates data in Cholesterol Patient Model
    Handles API requests from the front-end. This is the concrete implementation of the PatientViewSet
    """

    # List of all patients in the database (Model)
    queryset = CholesterolPatient.objects.all()
    patient_queryset = queryset
    # The class that serializes/deserializes data to/from front-end (handled by Django serializers)
    serializer_class = CholesterolPatientSerializer
    # The specific lookup fields to view/filter patient objects by
    lookup_field = 'id'
    filter_fields = ('original_patient',)

    def retrieve(self, request, id=None):
        """
        Based on an API GET request, this gets data for a particular CholesterolPatient in the database 
        (queryset) using its ID and returns a JSON response
        Called using root_url + '/CholesterolPatient/<id>/' 
        """
        try:
            original_patient = Patient.objects.get(id = id)
            chol_patient = CholesterolPatient.objects.get(original_patient = original_patient)
        # Otherwise return error
        except:
            return Response({'error': 'Invalid Patient ID'}, status = status.HTTP_400_BAD_REQUEST)

        response = CholesterolPatientSerializer(chol_patient).data
        response.update(PatientSerializer(original_patient).data)
        return Response(response, status=status.HTTP_200_OK)

    def partial_update(self, request, id=None):
        """
        Based on an API PATCH request, this partially updates a CholesterolPatient object with a given id
        Called using root_url + /CholesterolPatient/id/?<params>
        """
        try:
            # Get the parameters the API call wants to update
            
            # Update the parameters in the Model
            try:
                visible = request.query_params['visible']
                self.visibilityUpdated(visible, id)
            except:
                pass

            try:
                highlighted = request.query_params['highlighted']
                self.highlightedUpdated(highlighted, id)
            except:
                pass

            original_patient = Patient.objects.get(id = id)
            patient = CholesterolPatient.objects.get(original_patient = original_patient)
            prac = CholesterolPractitioner.objects.get(original_practitioner = original_patient.practitioner)
            prac.calculateAverageCholesterol()
            prac.getHighlighted()
            patient.save()

            response = CholesterolPatientSerializer(patient).data
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Invalid query - details not valid'}, status = status.HTTP_400_BAD_REQUEST)

    def visibilityUpdated(self, visible, id):
        """
        Function that takes visible value and then saves that to the patient
        """
        original_patient = Patient.objects.get(id = id)
        patient = CholesterolPatient.objects.get(original_patient = original_patient)
        patient.visible = visible
        patient.save()

    def highlightedUpdated(self, highlighted, id):
        """
        Function that takes highlighted value and then saves that to the patient
        """
        original_patient = Patient.objects.get(id = id)
        patient = CholesterolPatient.objects.get(original_patient = original_patient)
        patient.highlighted = highlighted
        patient.save()

class BloodPressurePractitionerViewSet(PractitionerViewSet):
    """
    Controller for CholesterolPractitioner - gets and updates data in Cholesterol Practitioner Model
    Handles API requests from the front-end. This is the concrete implementation of the PractitionerViewSet
    """

    # List of all practitioners in the database (Model)
    queryset = BloodPressurePractitioner.objects.all()
    practitioner_queryset = queryset
    # The class that serializes/deserializes data to/from front-end (handled by Django serializers)
    serializer_class = BloodPressurePractitionerSerializer
    # The specific lookup fields to view/filter practitioner objects by
    lookup_field = 'identifier'
    filter_fields = ('original_practitioner',)


    def retrieve(self, request, identifier = None):
        """
        Based on an API GET request, this gets data for a particular CholestrolPractitioner in the database 
        (queryset) using its ID and returns a JSON response
        Called using root_url + '/cholesterolpractitioner/<id>/' 
        """
        try:
            original_practitioner = Practitioner.objects.get(identifier = identifier)
            try:
                bp_practitioner = BloodPressurePractitioner.objects.get(original_practitioner = original_practitioner)
                bp_practitioner.save(request = 'get')
            except:
                try:
                    bp_practitioner = BloodPressurePractitioner(bp_prac_id = 0, original_practitioner = original_practitioner)
                except Exception as e:
                    print(e)
                bp_practitioner.save(request = 'get')
                bp_practitioner = BloodPressurePractitioner.objects.get(original_practitioner = original_practitioner)
            response = BloodPressurePractitionerSerializer(bp_practitioner).data
            response.update(PractitionerSerializer(original_practitioner).data)
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Practitioner not instantiated in Model yet'}, status = status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, identifier = None):
        """
        Based on an API PATCH request, this partially updates a practitioner object with a given id
        Called using root_url + /cholesterolpractitioner/id/?<params>
        """
        try:
            # Get the practitioner object by its identifier
            # original_prac = Practitioner.objects.get(identifier = identifier)
            # practitioner = CholesterolPractitioner.objects.get(original_practitioner = original_prac)

            # Update the fields in the Model
            try:
                refresh_rate = request.query_params['refresh_rate']
                self.refreshRateUpdated(refresh_rate, identifier)
            except:
                pass

            try:
                filter_bp = request.query_params['filter_bp_sys']
                self.filterBPSysUpdated(filter_bp, identifier)
                #practitioner.getHighlighted()
            except:
                pass

            try:
                filter_bp = request.query_params['filter_bp_dia']
                self.filterBPDiaUpdated(filter_bp, identifier)
                #practitioner.getHighlighted()
            except:
                pass
            
            original_prac = Practitioner.objects.get(identifier = identifier)
            practitioner = BloodPressurePractitioner.objects.get(original_practitioner = original_prac)
            practitioner.save(request = 'patch')
            response = BloodPressurePractitionerSerializer(practitioner).data
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Invalid query - details not valid'}, status = status.HTTP_400_BAD_REQUEST)

    def filterBPSysUpdated(self, filter_bp_x, identifier):
        """
        Function that takes filter_cholesterol value and then saves that to the practitioner
        """
        original_prac = Practitioner.objects.get(identifier = identifier)
        practitioner = BloodPressurePractitioner.objects.get(original_practitioner = original_prac)
        practitioner.filter_bp_x = int(filter_bp_x)
        practitioner.save(request='patch')

    def filterBPDiaUpdated(self, filter_bp_y, identifier):
        """
        Function that takes filter_cholesterol value and then saves that to the practitioner
        """
        original_prac = Practitioner.objects.get(identifier = identifier)
        practitioner = BloodPressurePractitioner.objects.get(original_practitioner = original_prac)
        practitioner.filter_bp_y = int(filter_bp_y)
        practitioner.save(request='patch')

    def refreshRateUpdated(self, refresh_rate, identifier):
        """
        Function that takes refresh_rate value and then saves that to the practitioner
        """
        original_prac = Practitioner.objects.get(identifier = identifier)
        practitioner = BloodPressurePractitioner.objects.get(original_practitioner = original_prac)
        practitioner.refresh_rate = int(refresh_rate)
        practitioner.save(request='patch')

class BloodPressurePatientViewSet(PatientViewSet):

    """
    Controller for CholesterolPatient - gets and updates data in Cholesterol Patient Model
    Handles API requests from the front-end. This is the concrete implementation of the PatientViewSet
    """

    # List of all patients in the database (Model)
    queryset = BloodPressurePatient.objects.all()
    patient_queryset = queryset
    # The class that serializes/deserializes data to/from front-end (handled by Django serializers)
    serializer_class = BloodPressurePatientSerializer
    # The specific lookup fields to view/filter patient objects by
    lookup_field = 'id'
    filter_fields = ('original_patient',)

    def retrieve(self, request, id=None):
        """
        Based on an API GET request, this gets data for a particular CholesterolPatient in the database 
        (queryset) using its ID and returns a JSON response
        Called using root_url + '/CholesterolPatient/<id>/' 
        """
        try:
            original_patient = Patient.objects.get(id = id)
            bp_patient = BloodPressurePatient.objects.get(original_patient = original_patient)
        # Otherwise return error
        except:
            return Response({'error': 'Invalid Patient ID'}, status = status.HTTP_400_BAD_REQUEST)

        response = BloodPressurePatientSerializer(bp_patient).data
        response.update(PatientSerializer(original_patient).data)
        return Response(response, status=status.HTTP_200_OK)

    def partial_update(self, request, id=None):
        """
        Based on an API PATCH request, this partially updates a CholesterolPatient object with a given id
        Called using root_url + /CholesterolPatient/id/?<params>
        """
        try:
            # Get the parameters the API call wants to update
            
            # Update the parameters in the Model
            try:
                visible = request.query_params['visible']
                self.visibilityUpdated(visible, id)
            except:
                pass

            try:
                num = request.query_params['latest_n']
                return Response(self.getNLatest(int(num), id), status=status.HTTP_200_OK)
            except:
                pass

            try:
                highlighted = request.query_params['highlighted']
                self.highlightedUpdated(highlighted, id)
            except:
                pass

            original_patient = Patient.objects.get(id = id)
            patient = BloodPressurePatient.objects.get(original_patient = original_patient)
            prac = BloodPressurePractitioner.objects.get(original_practitioner = original_patient.practitioner)
            # prac.getHighlighted()
            patient.save(request="")

            response = BloodPressurePatientSerializer(patient).data
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Invalid query - details not valid'}, status = status.HTTP_400_BAD_REQUEST)

    def getNLatest(self, n, id):
        """
        Function that takes visible value and then saves that to the patient
        """
        original_patient = Patient.objects.get(id = id)
        patient = BloodPressurePatient.objects.get(original_patient = original_patient)
        nlatest = patient.getNLatestSys(n)
        return nlatest[::-1]

    def visibilityUpdated(self, visible, id):
        """
        Function that takes visible value and then saves that to the patient
        """
        original_patient = Patient.objects.get(id = id)
        patient = BloodPressurePatient.objects.get(original_patient = original_patient)
        patient.visible = visible
        patient.save(request="")

    def highlightedUpdated(self, highlighted, id):
        """
        Function that takes highlighted value and then saves that to the patient
        """
        original_patient = Patient.objects.get(id = id)
        patient = BloodPressurePatient.objects.get(original_patient = original_patient)
        patient.highlighted = highlighted
        patient.save()

class SmokerPractitionerViewSet(PractitionerViewSet):
    """
    Controller for SmokerPractitioner - gets and updates data in Cholesterol Practitioner Model
    Handles API requests from the front-end. This is the concrete implementation of the PractitionerViewSet
    """

    # List of all practitioners in the database (Model)
    queryset = SmokerPractitioner.objects.all()
    practitioner_queryset = queryset
    # The class that serializes/deserializes data to/from front-end (handled by Django serializers)
    serializer_class = SmokerPractitionerSerializer
    # The specific lookup fields to view/filter practitioner objects by
    lookup_field = 'identifier'
    filter_fields = ('original_practitioner',)

    def retrieve(self, request, identifier = None):
        """
        Based on an API GET request, this gets data for a particular CholestrolPractitioner in the database 
        (queryset) using its ID and returns a JSON response
        Called using root_url + '/cholesterolpractitioner/<id>/' 
        """
        try:
            original_practitioner = Practitioner.objects.get(identifier = identifier)
            try:
                smoker_practitioner = SmokerPractitioner.objects.get(original_practitioner = original_practitioner)
                smoker_practitioner.save(request = 'get')
            except:
                try:
                    smoker_practitioner = SmokerPractitioner(smoker_prac_id = 0, original_practitioner = original_practitioner)
                except Exception as e:
                    print(e)
                smoker_practitioner.save(request = 'get')
                smoker_practitioner = SmokerPractitioner.objects.get(original_practitioner = original_practitioner)
            response = SmokerPractitionerSerializer(smoker_practitioner).data
            print(response)
            response.update(PractitionerSerializer(original_practitioner).data)
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Practitioner not instantiated in Model yet'}, status = status.HTTP_400_BAD_REQUEST)

class SmokerPatientViewSet(PatientViewSet):

    """
    Controller for CholesterolPatient - gets and updates data in Cholesterol Patient Model
    Handles API requests from the front-end. This is the concrete implementation of the PatientViewSet
    """

    # List of all patients in the database (Model)
    queryset = SmokerPatient.objects.all()
    patient_queryset = queryset
    # The class that serializes/deserializes data to/from front-end (handled by Django serializers)
    serializer_class = SmokerPatientSerializer
    # The specific lookup fields to view/filter patient objects by
    lookup_field = 'id'
    filter_fields = ('original_patient',)

    def retrieve(self, request, id=None):
        """
        Based on an API GET request, this gets data for a particular SmokerPatient in the database 
        (queryset) using its ID and returns a JSON response
        Called using root_url + '/SmokerPatient/<id>/' 
        """
        try:
            original_patient = Patient.objects.get(id = id)
            smoker_patient = SmokerPatient.objects.get(original_patient = original_patient)
        # Otherwise return error
        except:
            return Response({'error': 'Invalid Patient ID'}, status = status.HTTP_400_BAD_REQUEST)

        response = SmokerPatientSerializer(smoker_patient).data
        response.update(PatientSerializer(original_patient).data)
        return Response(response, status=status.HTTP_200_OK)

