import Controller from './View'
import axios from "axios";
import PatientCholesterolView from './PatientCholesterolView'
import patientBloodView from './PatientBloodView'

export default class PatientView {
  patientCholesterolController = new PatientCholesterolView();
  patientBloodController = new patientBloodView();
}
