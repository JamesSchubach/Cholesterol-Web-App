from django.db import models
import requests
import json

# Create your models here.
class Practitioner(models.Model):
    """
    Abstract model for the patient 
    """
    identifier = models.IntegerField(primary_key=True)

    # Gets a practitioner's patients and updates the patient_list and patient_ids variables
    def getFHIRPatients(self):
        """
        Getter function that gets the patients from the database relating to the practitioner
        """
        # Form URL for API call based on practitioner's ID - finds Encounters of the practitioner
        root_url = 'https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/'
        # encounters_url = root_url + "Encounter?participant={}&_include=Encounter.participant.individual&_include=Encounter.patient"
        # encounters_url = 'Encounter?participant.identifier=http://hl7.org/fhir/sid/us-npi|{}&_include=Encounter.participant.individual&_include=Encounter.patient'
        encounters_url = root_url + 'Encounter?_include=Encounter.participant.individual&_include=Encounter.patient&participant.identifier=http%3A%2F%2Fhl7.org%2Ffhir%2Fsid%2Fus-npi%7C{}'
        encounters_url = encounters_url.format(str(self.identifier))

        practitioner_encounters = requests.get(url=encounters_url).json()               
        encounter_data = practitioner_encounters['entry']

        # Loop through all encounters in the practitioner's history
        for entry in encounter_data:
            # Get the patient object
            item = entry['resource']
            patient_obj = item['subject']['reference']
            
            # Get the patient ID from the patient object
            patient_id = patient_obj.split('/')[1]
            p_list = []
            # If patient doesn't already exist in Practitioner's patients, add it and create the patient instance
            try:
                patient = Patient.objects.get(id = patient_id)
            except:
                patient_info = self.findFHIRPatientInfo(patient_id)
                self.createPatient(patient_info)
                
    # Finds a particular patient's info on the server given their patient ID
    def findFHIRPatientInfo(self, id):
        """
        Getter function that gets the patient from the database relating to the practitioner
        """
        patient_id_url = 'https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/Patient/' + id
        raw_data = requests.get(url = patient_id_url).json()
        
        # Some patients don't have prefixes
        try:
            prefix = raw_data['name'][0]['prefix'][0]
        except:
            prefix = ""

        patient_info = {
                'id': raw_data['id'],
                'givenName': raw_data['name'][0]['given'][0],
                'familyName': raw_data['name'][0]['family'],
                'prefixName': prefix,
                'birth_date':raw_data['birthDate'],
                'gender': raw_data['gender'],
                'city': raw_data['address'][0]['city'],
                'state': raw_data['address'][0]['state'],
                'country': raw_data['address'][0]['country'],
                # 'latest_chol': 0,
                # 'visible': True,
                # 'highlighted': False,
                'practitioner_identifier': self.identifier
            }
        
        return patient_info

    # Creates a patient for the practitioner
    def createPatient(self, info):
        """
        Simple function for creating a patient with the relating info
        """
        new_patient = Patient(info['id'], 
                        info['givenName'], 
                        info['familyName'], 
                        info['prefixName'], 
                        info['birth_date'], 
                        info['gender'],
                        info['city'],
                        info['state'],
                        info['country'],
                        # info['latest_chol'],
                        # info['visible'],
                        # info['highlighted'],
                        info['practitioner_identifier']
                        )
        new_patient.save()
        
    def save(self, *args, **kwargs):
        request = kwargs['request']

        super(Practitioner, self).save()
        if request == 'get':
            self.getFHIRPatients()
            # self.calculateAverageCholesterol()
        super(Practitioner, self).save()

class Patient(models.Model):
    """
    Abstract model for the patient 
    """
    id = models.IntegerField(primary_key=True)
    given_name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=100)
    prefix_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # self.getLatestChol()
        try:
            super(Patient, self).save(*args, **kwargs)
        except Exception as e:
            print(e)

class CholesterolPractitioner(models.Model):
    """
    Model for the concrete version of practitioner Model
    """
    chol_prac_id = models.IntegerField(primary_key=True)
    average_cholesterol = models.IntegerField(default=0)
    filter_cholesterol =  models.IntegerField(default=0)
    refresh_rate = models.IntegerField(default=30000)
    above_average_count = models.IntegerField(default=0)
    original_practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE, related_name='original_practitioner', default=00000)

    def getCholPatients(self):
        """
        Gets the cholesetrol patients, e.g. creates cholestrol patients for the cholesterol practitioner
        """
        # Go through all of practitioner's patients and create CholesterolPatients for all of them
        patients = Patient.objects.filter(practitioner = self.original_practitioner)
        num_patients = 0
        for patient in patients:
            new_chol_patient = CholesterolPatient(chol_patient_id = num_patients, original_patient = patient)
            new_chol_patient.save()
            num_patients += 1

    # This function goes through the patients and changes their highlight respectively
    def getHighlighted(self):
        """
        Function that changes the highlight of a the patients dependent on average cholesterol and filter
        """
        patients = Patient.objects.filter(practitioner = self.original_practitioner)
        print("called function")
        self.above_average_count = 0
        for patient in patients:
            new_chol_patient = CholesterolPatient.objects.get(original_patient = patient)
            if (self.filter_cholesterol < self.average_cholesterol) and (self.filter_cholesterol != 0):
                if (new_chol_patient.latest_chol > self.filter_cholesterol) and not new_chol_patient.highlighted:
                    # new_chol_patient.toggleHighlighted()
                    new_chol_patient.highlighted = True
                elif new_chol_patient.latest_chol < self.filter_cholesterol and new_chol_patient.highlighted:
                    # new_chol_patient.toggleHighlighted()
                    new_chol_patient.highlighted = False
            elif (self.filter_cholesterol >= self.average_cholesterol):
                if (new_chol_patient.latest_chol > self.filter_cholesterol) and not new_chol_patient.highlighted:
                    # new_chol_patient.toggleHighlighted()
                    new_chol_patient.highlighted = True
                    self.above_average_count += 1
                elif new_chol_patient.latest_chol < self.filter_cholesterol and new_chol_patient.highlighted:
                    # new_chol_patient.toggleHighlighted()
                    new_chol_patient.highlighted = False
            else:
                if (new_chol_patient.latest_chol > self.average_cholesterol) and not new_chol_patient.highlighted:
                    # new_chol_patient.toggleHighlighted()
                    new_chol_patient.highlighted = True
                    self.above_average_count += 1
                elif (new_chol_patient.latest_chol < self.average_cholesterol) and new_chol_patient.highlighted:
                    # new_chol_patient.toggleHighlighted()
                    new_chol_patient.highlighted = False
            new_chol_patient.save()
        self.save(request="")
        
    # Calculates average cholesterol of all the practitioner's chosen (i.e. VISIBLE) patients
    def calculateAverageCholesterol(self):
        """
        Function that calculates the average cholesterol of the patients of the practitioner
        """
        total_cholesterol = 0
        # Potential Speed-up
            # self.savePatients()
            # patient_list = self.fromJson()
        patient_list = Patient.objects.filter(practitioner = self.original_practitioner.identifier)
        num_patients = 0
        # Loop through all Patient instances in patient_list
        for patient in patient_list:
            chol_patient = CholesterolPatient.objects.get(original_patient = patient)
            # If patient is set to VISIBLE, add their cholesterol value to total practitioner cholesterol
            if chol_patient.visible:
                cholesterol_value = chol_patient.getLatestChol()
                # If patient has a 0 cholesterol_value, it means no records exist - so ignore them in calculations
                if cholesterol_value != 0:
                    total_cholesterol += int(cholesterol_value)
                    num_patients += 1

        # Compute average cholesterol if num_patients > 0, otherwise set it to 0 as no cholesterol records exist for patients
        if num_patients != 0:
            self.average_cholesterol = total_cholesterol / num_patients
        else:
            self.average_cholesterol = 0
        return self.average_cholesterol

    def save(self, *args, **kwargs):
        """
        Required function to save the patient model to the database
        """
        request = kwargs['request']
        try:
            super(CholesterolPractitioner, self).save()
        except Exception as e:
            print(e)
        
        if request == 'get':
            self.getCholPatients()
            self.calculateAverageCholesterol()
            self.getHighlighted()
        elif request == 'patch':
            self.getHighlighted()
        super(CholesterolPractitioner, self).save()

class CholesterolPatient(models.Model):
    """
    Model for the concrete version of Patient Model
    """
    chol_patient_id = models.IntegerField(primary_key=True)
    latest_chol = models.IntegerField(default=0)
    visible = models.BooleanField(default=True)
    highlighted = models.BooleanField(default=False)
    original_patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='original_patient', default=00000)
    latest_time = models.CharField(default="", max_length=300)

    # Toggles the visibility of the patient
    def toggleVisibility(self):
        """
        Simple function that toggles the visibility of the patient
        """
        if self.visible:
            self.visible = False
        else:
            self.visible = True
        return self.visible

    # Toggles highlighted field of patient
    def toggleHighlighted(self):
        """
        Simple function that toggles the highlighted of the patient
        """
        if self.highlighted:
            self.highlighted = False
        else:
            self.highlighted = True
        return self.highlighted

    # Gets the patient's latest cholesterol value
    def getLatestChol(self):
        """
        Getter function, get the latest cholesterol value of the patient
        """
        # URL for API call is formed - sorting by descending date order and getting only the first 3 entries
        root_url = 'https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/'
        search_url= root_url + "Observation?patient={}&code=2093-3&_sort=-date&_count=3"
        search_url = search_url.format(str(self.original_patient.id))

        raw_data = requests.get(url = search_url).json()

        # Find cholesterol value or set it to 0 if no records exist for patient
        try:
            entry = raw_data['entry']
            latest_cholesterol = entry[0]

            resource = latest_cholesterol['resource']
            time = resource['effectiveDateTime']
            cholesterol_value = resource['valueQuantity']['value']
        except:
            cholesterol_value = 0
            time = ""
        
        self.latest_time = time
        self.latest_chol = cholesterol_value

        return self.latest_chol

    def save(self, *args, **kwargs):
        """
        Required function to save the patient model to the database
        """
        self.getLatestChol()
        try:
            super(CholesterolPatient, self).save(*args, **kwargs)
        except Exception as e:
            print(e)

class BloodPressurePractitioner(models.Model):
    """
    Model for the concrete version of practitioner Model
    """
    bp_prac_id = models.IntegerField(primary_key=True)
    filter_bp_x =  models.IntegerField(default=0)
    filter_bp_y =  models.IntegerField(default=0)
    highlighted_sys_count = models.IntegerField(default=0)
    highlighted_dia_count = models.IntegerField(default=0)
    original_practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE, related_name='bp_original_practitioner', default=00000)
    
    #Get refresh rate from cholestorol
    refresh_rate = models.IntegerField(default=30000)

    def getBPPatients(self):
        """
        Gets the cholesetrol patients, e.g. creates cholestrol patients for the cholesterol practitioner
        """
        # Go through all of practitioner's patients and create CholesterolPatients for all of them
        patients = Patient.objects.filter(practitioner = self.original_practitioner)
        num_patients = 0
        for patient in patients:
            new_bp_patient = BloodPressurePatient(bp_patient_id = num_patients, original_patient = patient)
            new_bp_patient.save(request="get")
            num_patients += 1

    # # This function goes through the patients and changes their highlight respectively
    def getHighlighted(self):
        """
        Function that changes the highlight of a the patients dependent on average cholesterol and filter
        """
        patients = Patient.objects.filter(practitioner = self.original_practitioner)
        self.highlighted_sys_count = 0
        self.highlighted_dia_count = 0
        for patient in patients:
            new_bp_patient = BloodPressurePatient.objects.get(original_patient = patient)
            if new_bp_patient.latest_sys_bp > self.filter_bp_x:
                new_bp_patient.highlighted_sys = True
                self.highlighted_sys_count += 1
            if new_bp_patient.latest_dia_bp > self.filter_bp_y:
                new_bp_patient.highlighted_dia = True
                self.highlighted_dia_count += 1
            new_bp_patient.save(request="")
        self.save(request="")


    # def getSysHighlighted(self):
    #     """
    #     Function that changes the highlight of a the patients dependent on average cholesterol and filter
    #     """
    #     patients = Patient.objects.filter(practitioner = self.original_practitioner)
    #     self.highlighted_dia_count = 0
    #     for patient in patients:
    #         new_bp_patient = BloodPressurePatient.objects.get(original_patient = patient)
    #         if new_bp_patient.latest_dia_bp > self.filter_bp_y:
    #             new_bp_patient.highlighted_dia = True
    #             self.highlighted_dia_count += 1
    #         new_bp_patient.save(request="")
    #     self.save(request="")
 

        
    def save(self, *args, **kwargs):
        """
        Required function to save the patient model to the database
        """
        request = kwargs['request']
        try:
            super(BloodPressurePractitioner, self).save()
        except Exception as e:
            print(e)
        
        if request == 'get':
            self.getBPPatients()
            self.getHighlighted()
        elif request == 'patch':
            self.getHighlighted()
        super(BloodPressurePractitioner, self).save()

class BloodPressurePatient(models.Model):
    """
    Model for the concrete version of Patient Model
    """
    bp_patient_id = models.IntegerField(primary_key=True)
    latest_sys_bp = models.IntegerField(default=0)
    latest_dia_bp = models.IntegerField(default=0)
    visible = models.BooleanField(default=True)
    highlighted_sys = models.BooleanField(default=False)
    highlighted_dia = models.BooleanField(default=False)
    original_patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='bp_original_patient', default=00000)
    latest_time = models.CharField(default="", max_length=300)


    # Toggles the visibility of the patient
    def toggleVisibility(self):
        """
        Simple function that toggles the visibility of the patient
        """
        if self.visible:
            self.visible = False
        else:
            self.visible = True
        return self.visible

    # Toggles highlighted field of patient
    def toggleHighlighted(self):
        """
        Simple function that toggles the highlighted of the patient
        """
        if self.highlighted:
            self.highlighted = False
        else:
            self.highlighted = True
        return self.highlighted

    def getNLatestSys(self, n):
        """
        Getter function, get the latest cholesterol value of the patient
        """
        # URL for API call is formed - sorting by descending date order and getting only the first 3 entries
        root_url = 'https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/'
        search_url= root_url + "Observation?patient={}&code=55284-4&_sort=-date&_count=3"
        search_url = search_url.format(str(self.original_patient.id))

        raw_data = requests.get(url = search_url).json()

        # Find cholesterol value or set it to 0 if no records exist for patient
        latest_sys_bp_list = []
        entry = raw_data['entry']
        for x in range(0, n):
            try:
                
                latest_bp = entry[x]

                resource = latest_bp['resource']
                time = resource['effectiveDateTime']
                resource = resource['component']
                latest_sys_bp = resource[1]['valueQuantity']['value']
                
            except:
                latest_sys_bp = 0
            
            latest_sys_bp_list.append((latest_sys_bp, time))

        return latest_sys_bp_list


    # Gets the patient's latest cholesterol value
    def getLatestSys(self):
        """
        Getter function, get the latest cholesterol value of the patient
        """
        # URL for API call is formed - sorting by descending date order and getting only the first 3 entries
        root_url = 'https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/'
        search_url= root_url + "Observation?patient={}&code=55284-4&_sort=-date&_count=3"
        search_url = search_url.format(str(self.original_patient.id))

        raw_data = requests.get(url = search_url).json()

        # Find cholesterol value or set it to 0 if no records exist for patient
        try:
            entry = raw_data['entry']
            latest_bp = entry[0]

            resource = latest_bp['resource']
            time = resource['effectiveDateTime']
            resource = resource['component']
            latest_sys_bp = resource[1]['valueQuantity']['value']
        except:
            time = ""
            latest_sys_bp = 0
        
        self.latest_time = time
        self.latest_sys_bp = latest_sys_bp

        return latest_sys_bp

    def getLatestDia(self):
        """
        Getter function, get the latest cholesterol value of the patient
        """
        # URL for API call is formed - sorting by descending date order and getting only the first 3 entries
        root_url = 'https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/'
        search_url= root_url + "Observation?patient={}&code=55284-4&_sort=-date&_count=3"
        search_url = search_url.format(str(self.original_patient.id))

        raw_data = requests.get(url = search_url).json()

        # Find cholesterol value or set it to 0 if no records exist for patient
        try:
            entry = raw_data['entry']
            latest_bp = entry[0]

            resource = latest_bp['resource']
            time = resource['effectiveDateTime']
            resource = resource['component']
            latest_dia_bp = resource[0]['valueQuantity']['value']
        except:
            latest_dia_bp = 0
            time = ""

        self.latest_time = time
        self.latest_dia_bp = latest_dia_bp

        return latest_dia_bp

    def save(self, *args, **kwargs):
        """
        Required function to save the patient model to the database
        """
        request = kwargs['request']

        if request == 'get':
            self.getLatestDia()
            self.getLatestSys()
        try:
            super(BloodPressurePatient, self).save()
        except Exception as e:
            print(e)

class SmokerPractitioner(models.Model):
    """
    Model for the concrete version of practitioner Model
    """
    smoker_prac_id = models.IntegerField(primary_key=True)
    non_smoker_count = models.IntegerField(default=0)
    original_practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE, related_name='smoker_original_practitioner', default=00000)

    def getSmokerPatients(self):
        """
        Gets the smoker patients, e.g. creates smoker patients for the smoker practitioner
        """
        # Go through all of practitioner's patients and create CholesterolPatients for all of them
        patients = Patient.objects.filter(practitioner = self.original_practitioner)
        num_patients = 0
        for patient in patients:
            new_smoker_patient = SmokerPatient(smoker_patient_id = num_patients, original_patient = patient)
            new_smoker_patient.save()
            num_patients += 1

    # This function goes through the patients and changes their highlight respectively
    def getNonSmokerCount(self):
        """
        Function that gets a count of all the patients that are smokers
        """
        patients = Patient.objects.filter(practitioner = self.original_practitioner)
        self.non_smoker_count = 0
        for patient in patients:
            smoker_patient = SmokerPatient.objects.get(original_patient = patient)
            if smoker_patient.smoker_status == "Never smoker":
                self.non_smoker_count += 1

        return self.non_smoker_count
        
    def save(self, *args, **kwargs):
        """
        Required function to save the patient model to the database
        """
        request = kwargs['request']
        try:
            super(SmokerPractitioner, self).save()
        except Exception as e:
            print(e)
        
        if request == 'get':
            self.getSmokerPatients()
            self.getNonSmokerCount()
        elif request == 'patch':
            self.getNonSmokerCount()
        super(SmokerPractitioner, self).save()

class SmokerPatient(models.Model):
    """
    Model for the abstract Smoker version of Patient Model
    """
    smoker_patient_id = models.IntegerField(primary_key=True)
    smoker_status = models.CharField(max_length=100)
    original_patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='smoker_original_patient', default=00000)

    # Gets the patient's latest cholesterol value
    def getSmokerStatus(self):
        """
        Getter function, get the latest smoker status of the patient
        """
        # URL for API call is formed - sorting by descending date order and getting only the first 3 entries
        root_url = 'https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/'
        search_url= root_url + "Observation?patient={}&code=72166-2&_sort=-date&_count=3"
        search_url = search_url.format(str(self.original_patient.id))

        raw_data = requests.get(url = search_url).json()

        # Find cholesterol value or set it to 0 if no records exist for patient
        try:
            entry = raw_data['entry']
            latest_cholesterol = entry[0]

            resource = latest_cholesterol['resource']
            smoker_status = resource['valueCodeableConcept']['text']
        except:
            smoker_status = "No records found"

        self.smoker_status = smoker_status

        return self.smoker_status

    def save(self, *args, **kwargs):
        """
        Required function to save the patient model to the database
        """
        self.getSmokerStatus()
        try:
            super(SmokerPatient, self).save(*args, **kwargs)
        except Exception as e:
            print(e)
