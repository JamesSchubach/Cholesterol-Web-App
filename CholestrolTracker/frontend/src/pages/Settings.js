import React, { useState, useEffect } from "react";
import axios from "axios";
import { Modal, Button, Form, Dropdown, ButtonGroup } from "react-bootstrap";
import {patientController, practitionerController} from '../views/View';

const Home = (props) => {
  
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

    let cholesterolFilter = "";
    let sysFilter = "";
    let diaFilter = "";
  
    const handleHidePatient = (patient, e, type) => {
      props.updatePatientVisibliity(patient.visible, patient.id, type);
    };
  
    const handleSubmit = () => {
      props.updateFilterCholesterol(cholesterolFilter);
    };

    const updateSysFilter = () => {
        props.updateSysFilter(sysFilter);
    }

    const updateDiaFilter = () => {
      props.updateDiaFilter(diaFilter);           
  }

    const setSysZero = () => {
        props.updateSysFilter(0);
    };

    const setDiaZero = () => {
      props.updateDiaFilter(0);
  };
  
    const setZero = () => {
      props.updateFilterCholesterol(0);
    };
  
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

    const getListOfItem = (data) =>{
        let listOfItems =  data.map((patient, index) => { 
          return (
            <tr style={{ color: "black" }}>
              <th scope="row"> {index} </th>
              <td> {patient.id}</td>
              <td> {patient.given_name} {patient.family_name}</td>
              <td> {patient.latest_chol == 0 ? '✗' : '✓'}</td>
              <td> {bloodPatients[index].latest_sys_bp == 0 ? '✗' : '✓'}</td>
              <td>
                <input
                  type="checkbox"
                  checked={patient.visible}
                  onChange={(e) => {
                    handleHidePatient(patient, e, 'chol');
                  }}
                />
              </td>

              <td>
                <input
                  type="checkbox"
                  checked={bloodPatients[index].visible}
                  onChange={(e) => {
                    handleHidePatient(bloodPatients[index], e, 'blood');
                  }}
                />
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
<div>
<div class="row" >
          <div class="col">
            <Dropdown style={{marginTop: '5px'}}>
              <Dropdown.Toggle variant="success" id="dropdown-basic">
                Refresh Rate
              </Dropdown.Toggle>
              <Dropdown.Menu>
                <Dropdown.Item onClick={()=>{props.updateRefreshRate(5000)}}>
                  5 seconds
                </Dropdown.Item>
                <Dropdown.Item onClick={()=>{props.updateRefreshRate(10000)}}>
                  10 seconds{" "}
                </Dropdown.Item>
                <Dropdown.Item onClick={()=>{props.updateRefreshRate(30000)}}>
                  30 seconds
                </Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
          </div>

          <div class="col" style={{display: 'flex'}}>
            <Form style={{display: 'flex', height:'45px'}}>
              <Form.Group controlId="formBasicEmail">
                <Form.Control
                  type="input"
                  placeholder={props.filter}
                  onChange={(e) => {
                    cholesterolFilter = e.target.value;
                  }}
                />
              </Form.Group>
              <ButtonGroup size="sm" className="mb-2">
              <Button variant="primary" onClick={handleSubmit} style={{fontSize:'10px'}}>
                Update Cholesterol Filter
              </Button>
              <Button variant="danger" onClick={setZero} >
                  ✗
              </Button>
                </ButtonGroup>
            </Form>
            </div>

            <div class="col" style={{display: 'flex'}}>
            <Form style={{display: 'flex', height:'45px'}}>
              <Form.Group controlId="formBasicEmail">
                <Form.Control
                  type="input"
                  placeholder={props.sysFilter}
                  onChange={(e) => {sysFilter = e.target.value}}
                />
              </Form.Group>
              <ButtonGroup size="sm" className="mb-2">
              <Button variant="primary" onClick={updateSysFilter} style={{fontSize:'10px'}}>
                Update Systolic Filter
              </Button>
              <Button variant="danger" onClick={setSysZero} >
                  ✗
              </Button>
                </ButtonGroup>
            </Form>
            </div>

            <div class="col" style={{display: 'flex'}}>
            <Form style={{display: 'flex', height:'45px'}}>
              <Form.Group controlId="formBasicEmail">
                <Form.Control
                  type="input"
                  placeholder={props.diaFilter}
                  onChange={(e) => {diaFilter = e.target.value}}
                />
              </Form.Group>
              <ButtonGroup size="sm" className="mb-2">
              <Button variant="primary" onClick={updateDiaFilter} style={{fontSize:'10px'}}>
                Update Diastolic Filter
              </Button>
              <Button variant="danger" onClick={setDiaZero} >
                  ✗
              </Button>
                </ButtonGroup>
            </Form>
          </div>
        </div>


        <table class="table table-hover">
          <thead class="thead-dark">
            <tr>
              <th scope="col">#</th>
              <th scope="col">ID</th>
              <th scope="col">Name</th>
              <th scope="col">Cholesterol Data</th>
              <th scope="col">Blood Data</th>
              <th scope="col" >Cholesterol Visibility</th>
              <th scope="col" >Blood Visibility</th>
            </tr>
          </thead>
  
          <tbody>{listItems}</tbody>
        </table>
       
      </div>
    );
  };

  export default Home