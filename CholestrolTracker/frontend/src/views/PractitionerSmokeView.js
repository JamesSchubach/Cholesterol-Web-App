import Controller from './View'
import axios from "axios";


export default class PractitionerSmokeView {

    getSmokerPractitioner = async (id) =>{
        const result = await axios('http://localhost:8000' + "/api/smokerpractitioner/" + id)
        return result.data
      }

}


