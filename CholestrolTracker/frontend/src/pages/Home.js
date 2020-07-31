import React, { useState, useEffect } from "react";
import axios from "axios";
import { Modal, Button, Form, Dropdown } from "react-bootstrap";
import {patientController, practitionerController} from '../views/View';

const Home = (props) => {
    const handleShow = (patient, bloodData) => {
    //   getGraph(patient.id);
       let graph = patientController.patientBloodController.getPatientBloodResults(patient.id)
        Promise.resolve(graph).then((data)=>{
            patient.graph = data
            props.setPatient(patient);
            props.setShow(true);
        })
    
    };
  
    const [cholesterolPatients, setCholesterolPatients] = useState([])
    const [bloodPatients, setBloodPatients] = useState([])
    let listItems = []

    let counter = -1;
    let cholesterolPatientList = []
    let bloodPatientList = []

    useEffect(() => {
        getCholesterolData();
        getBloodData();
    }, []);
  
    const getCholesterolData = () => {
        if(props.practitioner){
        for(var i in props.practitioner.patients){
            cholesterolPatientList.push(patientController.patientCholesterolController.getCholPatient(props.practitioner.patients[i].id))
            }}
        Promise.all(cholesterolPatientList).then((data)=>{
            setCholesterolPatients(data)
        })
    }

    const getBloodData = () => {
     if(props.practitioner){
        for (var i in props.practitioner.patients){
                bloodPatientList.push(patientController.patientBloodController.getBloodPatient(props.practitioner.patients[i].id))
        }}
      Promise.all(bloodPatientList).then((data)=>{
        setBloodPatients(data)
        })
    }

    // const getGraph  = (id) =>{
    //     let graph = patientController.getPatientBloodResults(id)
    //     Promise.resolve(graph).then((data)=>{
    //         console.log('graph ', data)
    //     })
    // }
    const getListOfItem = (data) =>{
        let listOfItems =  data.map((patient, index) => { 
              counter += 1;
              return (
                <tr >
                  <th scope="row"> {counter} </th>
                  <td> {patient.id}</td>
                  <td> {patient.given_name} {patient.family_name}</td>
                   <td> {patient.latest_time}</td>
                  {patient.visible ? 
                   <td style={{ color: patient.highlighted ? "red" : "black" }} > {patient.latest_chol + "mg/dL"} </td>
                  : <td>--</td>}

                {bloodPatients[index].visible ? 
                  <><td style={{ color: bloodPatients[index].highlighted_sys ? "purple" : "black" }}> {bloodPatients[index].latest_sys_bp + "mmHg"}</td>
                  <td style={{ color: bloodPatients[index].highlighted_dia ? "purple" : "black" }}> {bloodPatients[index].latest_dia_bp + "mmHg"}</td></>
                    : <><td>--</td><td>--</td></>
                }
                <td>{bloodPatients[index].latest_time}</td>
                <td>
                    <a
                      class="btn btn-secondary btn-lg active"
                      role="button"
                      aria-pressed="true"
                      onClick={() => handleShow(patient, bloodPatients[index])}
                    >
                      Details
                    </a>{" "}
                  </td>

                </tr>
              );
          });
          listItems = listOfItems;
    }

    if(cholesterolPatients.length > 0 && bloodPatients.length > 0 ){
        getListOfItem(cholesterolPatients)
    }
  

    return (
      <table class="table table-hover">
        <thead class="thead-dark">
          <tr>
            <th scope="col">#</th>
            <th scope="col">ID</th>
            <th scope="col">Name</th>
            <th scope="col">Cholesterol</th>
            <th scope="col">Cholesterol Time</th>
            <th scope="col">Systolic BP</th>
            <th scope="col">Diastolic BP</th>
            <th scope="col">Blood Test Time</th>
            <th scope="col" style={{ width: "15" }}></th>
          </tr>
        </thead>
  
        <tbody>{listItems}</tbody>
      </table>
    );
  };

  export default Home