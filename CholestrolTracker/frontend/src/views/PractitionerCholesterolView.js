import Controller from './View'
import axios from "axios";


export default class PractitionerCholesterolView {

       updateFilterCholesterol = async (filter, id) => {
        const response = await axios.patch(
          'http://localhost:8000' + "/api/cholesterolpractitioner/" + id + "/?filter_cholesterol=" + filter
        );
      };

       getCholPractitioner = async (id) =>{
        const result = await axios('http://localhost:8000' + "/api/cholesterolpractitioner/" + id)
        return result.data
      }
      
}


