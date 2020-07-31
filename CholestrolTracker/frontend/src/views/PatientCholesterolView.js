import Controller from './View'
import axios from "axios";



export default class PatientCholesterolView {

    getCholPatient = async (id) =>{
        const patient = await axios("http://localhost:8000/api/cholesterolpatient/"+ id)
        return patient.data
        }

    updatePatientVisibliity = async (visibilty, id) => {
        let inverseVisibilty = !visibilty
        let newVisbility = capitalize(inverseVisibilty.toString());
    
        function capitalize(string) {
            return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
        }
    
        const response = await axios.patch(
            'http://localhost:8000' + "/api/cholesterolpatient/" + id + "/?visible=" + newVisbility
        );
        };

}