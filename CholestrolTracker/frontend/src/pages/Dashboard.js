import React, { useState, useEffect } from "react";
import axios from "axios";
import { Modal, Button, Form, Dropdown } from "react-bootstrap";
import {patientController, practitionerController} from '../views/View';
import Navbar from './Navbar'
import Settings from './Settings'
import PatientModal from './PatientModal'
import Home from './Home'
import CholestrolGraph from './CholesterolGraph'

const Dashboard = () => {
  const [page, setPage] = useState("Home");
  const [practitioner, setPractitioner] = useState({});
  const [cholPractitioner, setCholPractitioner] = useState({})
  const [bloodPracitioner, setBloodPracitioner] = useState({})
  const [smokePractitioner, setSmokePractitioner] = useState({})
  const [patient, setPatient] = useState({});
  const [loading, setLoading] = useState(true);
  const [timer, setTimer] = useState();
  const [filter, setFilter] = useState();
  const [sysFilter, setSysFilter] = useState();
  const [diaFilter, setDiaFilter] = useState();
  const [show, setShow] = useState(false);
  const url = window.location.origin;
  const id = window.location.pathname.substring(11,window.location.pathname.length - 1);
  const [refreshRate, setRefreshRate] = useState(0);

  // useEffect(() => {
  //   updateData();
  // }, [loading]);

  useEffect(() => {
    getData();
    getCholPractitioner();
    getBloodPractitioner();
    getSmokerPractitioner();
  }, []);

  const updateRefreshRate = async (newRate) => {
    setLoading(true);
    practitionerController.updateRefreshRate(newRate, id)
    setRefreshRate(newRate);
    updateData();
  };

  const updateFilterCholesterol = async (filter) => {
    setLoading(true);
    practitionerController.practitionerCholesterolController.updateFilterCholesterol(filter, id)
    updateData();
  };

  const updateDiaFilter = async (filter) =>{
    setLoading(true);
    practitionerController.practitionerBloodController.updateFilterDiastolic(filter, id)
    updateData();
  }

  const updateSysFilter = async (filter) =>{
    setLoading(true);
    practitionerController.practitionerBloodController.updateFilterSystolic(filter, id)
    updateData();
  }

  const updatePatientVisibliity = async (visibilty, id, type) => {
    setLoading(true);
    if(type == 'blood'){
      patientController.patientBloodController.updateBloodPatientVisibliity(visibilty, id)
    }
    if(type== 'chol'){
      patientController.patientCholesterolController.updatePatientVisibliity(visibilty, id)
    }
    updateData();
  };

  const updateData = async () =>{
    const result = await axios(url + "/api/practitioner/" + id);
    // let loadingArray = [getCholPractitioner(), getBloodPractitioner(), getSmokerPractitioner(), result]
    // Promise.all(loadingArray).then((data)=>{
      setPractitioner(result.data);
      setLoading(false);
    // })

  }

  const getData = async () => {
    setLoading(true);
    const result = await axios(url + "/api/practitioner/" + id);
    setPractitioner(result.data);
    if(refreshRate > 0){
      window.clearTimeout(timer)
      setTimer(window.setTimeout(() => {getData();}, refreshRate));
    }
    setLoading(false);
  };

  const getCholPractitioner = async () =>{
    let current = refreshRate
    practitionerController.practitionerCholesterolController.getCholPractitioner(id).then((data)=>{
      if (current != data.refresh_rate){
        setRefreshRate(data.refresh_rate);
      }
      setFilter(data.filter_cholesterol)
      setCholPractitioner(data)
        getData();
    })
  }

  const getBloodPractitioner = async () =>{
    practitionerController.practitionerBloodController.getBloodPractitioner(id).then((data)=>{
      setSysFilter(data.filter_bp_x)
      setDiaFilter(data.filter_bp_y)
      setBloodPracitioner(data)
    })
  }

  const getSmokerPractitioner = async () =>{
    practitionerController.practitionerSmokeController.getSmokerPractitioner(id).then((data)=>{
      setSmokePractitioner(data)
    })
  }

  const renderSwitch = (param) => {
    switch(param) {
      case 'Home':
        return (
          <Home
          practitioner={practitioner}
          setShow={setShow}
          setPatient={setPatient}
        />
        );
        case 'Settings':
          return (
            <Settings
            practitioner={practitioner}
            updateFilterCholesterol={updateFilterCholesterol}
            updateDiaFilter={updateDiaFilter}
            updateSysFilter={updateSysFilter}
            updatePatientVisibliity={updatePatientVisibliity}
            updateRefreshRate={updateRefreshRate}
            filter={filter}
            sysFilter={sysFilter}
            diaFilter={diaFilter}
          />
          );
      case 'Graph':
        return <CholestrolGraph
        cholPractitioner={cholPractitioner}
        bloodPracitioner={bloodPracitioner}
        smokePractitioner={smokePractitioner}
        practitioner={practitioner}
        setShow={setShow}
        setPatient={setPatient}/>
      default:
        return 'Home';
    }
  }

  if (loading) {
    return <h1></h1>;
  } else {
    return (
      <div>
        <Navbar setPage={setPage} page={page} />
       {renderSwitch(page)}
        <PatientModal show={show} setShow={setShow} patient={patient} />
      </div>
    );
  }
};




export default Dashboard;
