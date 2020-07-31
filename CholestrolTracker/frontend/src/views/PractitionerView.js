import Controller from './View'
import axios from "axios";
import PractitionerCholesterolView from './PractitionerCholesterolView'
import PractitionerBloodView from './PractitionerBloodView'
import PractitionerSmokeView from './PractitionerSmokeView'



export default class PractitionerView {
      practitionerCholesterolController = new PractitionerCholesterolView();
      practitionerBloodController = new PractitionerBloodView();
      practitionerSmokeController = new PractitionerSmokeView();


       updateRefreshRate = async (newRate, id) => {
        const response = await axios.patch(
          'http://localhost:8000' + "/api/cholesterolpractitioner/" + id + "/?refresh_rate=" + newRate
        );
      };

      }


