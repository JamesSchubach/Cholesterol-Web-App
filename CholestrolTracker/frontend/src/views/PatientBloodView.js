import Controller from './View'
import axios from "axios";



export default class PatientBloodView {

    updateBloodPatientVisibliity = async (visibilty, id) => {
        let inverseVisibilty = !visibilty
        let newVisbility = capitalize(inverseVisibilty.toString());
    
        function capitalize(string) {
          return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
        }
    
        const response = await axios.patch(
          'http://localhost:8000' + "/api/bloodpressurepatient/" + id + "/?visible=" + newVisbility
        );
      };
    
      getBloodPatient = async (id) =>{
        const patient = await axios("http://localhost:8000/api/bloodpressurepatient/"+ id)
        return patient.data
        }
    
      getPatientBloodResults = async(id)=>{
        const patient = await axios.patch('http://localhost:8000/api/bloodpressurepatient/'+id+'/?latest_n=5')
        return patient.data
      }

}