import Controller from './View'
import axios from "axios";


export default class PractitionerBloodView {

      updateFilterSystolic = async (filter, id) => {
        const response = await axios.patch(
          'http://localhost:8000' + "/api/bloodpressurepractitioner/" + id + "/?filter_bp_sys=" + filter
        );
      };

      updateFilterDiastolic = async (filter, id) => {
        const response = await axios.patch(
          'http://localhost:8000' + "/api/bloodpressurepractitioner/" + id + "/?filter_bp_dia=" + filter
        );
      };
      
      getBloodPractitioner = async (id) =>{
        const result = await axios('http://localhost:8000' + "/api/bloodpressurepractitioner/" + id)
        return result.data
      }

}


