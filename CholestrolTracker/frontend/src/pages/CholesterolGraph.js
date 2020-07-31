import React, { useState, useEffect } from "react";
import axios from "axios";
import { Modal, Button, Form, Dropdown } from "react-bootstrap";
import {patientController, practitionerController} from '../views/View';
import Chart from "react-apexcharts";

const CholestrolGraph = (props) => {
    const handleShow = (patient) => {
      props.setPatient(patient);
      props.setShow(true);
    };
    const id = window.location.pathname.substring(11,window.location.pathname.length - 1);

  
    const [loading, setloading] = useState(true)
    const [patientArray, setPatientArray] = useState([])
    const [cholesterolArray, setCholesterolArray] = useState([])

    const [smokerCount, setSmokerCount] = useState(null)
    const [sysCount, setSysCount]=useState(null)
    const [diaCount, setDiaCount]=useState(null)
    const [cholCount, setCholCount]=useState(null)


    let cholesterolPatientList = []
    let graphData = {'patients':patientArray, 'cholesterol':cholesterolArray}

    useEffect(() => {
      getData();
      getCholPractitioner();
      getBloodPractitioner();
      getSmokerPractitioner();
    }, []);
  
    const getData = () => {
    if(props.practitioner){
      for(var i in props.practitioner.patients){
        cholesterolPatientList.push(patientController.patientCholesterolController.getCholPatient(props.practitioner.patients[i].id))
        }}
  
      Promise.all(cholesterolPatientList).then((data)=>{
          let patients = patientArray
          let cholesterol = cholesterolArray;
          data.forEach(i =>{   
            if(i.latest_chol  > 0){
              patients.push(i.given_name)
              cholesterol.push(i.latest_chol)
            }         
          })
          setPatientArray(patients)
          setCholesterolArray(cholesterol)
          setloading(false)
      })
    }


    const getCholPractitioner = async () =>{
      practitionerController.practitionerCholesterolController.getCholPractitioner(id).then((data)=>{
        setCholCount(data.above_average_count)
      })
    }
  
    const getBloodPractitioner = async () =>{
      practitionerController.practitionerBloodController.getBloodPractitioner(id).then((data)=>{
        setSysCount(data.highlighted_sys_count)
        setDiaCount(data.highlighted_dia_count)
      })
    }
  
    const getSmokerPractitioner = async () =>{
      practitionerController.practitionerSmokeController.getSmokerPractitioner(id).then((data)=>{
        setSmokerCount(data.non_smoker_count)
      })
    }


    let options = {
      chart: {
        height: 350,
        type: 'bar',
      },
      plotOptions: {
        bar: {
          columnWidth: '50%',
          endingShape: 'rounded'  
        }
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        width: 2
      },
      grid: {
        row: {
          colors: ['#fff', '#f2f2f2']
        }
      },
      // grid: {
      //   row: {
      //     colors: ['#8bfce6', '#18BC9C']
      //   }
      // },
      xaxis: {
        labels: {
          rotate: -45
        },
        categories: graphData.patients,
        tickPlacement: 'on'
      },
      yaxis: {
        title: {
          text: 'Cholesterol',
        },
      },
      fill: {
        type: 'gradient',
        gradient: {
          shade: 'light',
          type: "horizontal",
          shadeIntensity: 0.25,
          gradientToColors: undefined,
          inverseColors: true,
          opacityFrom: 0.85,
          opacityTo: 0.85,
          stops: [50, 0, 100]
        },
      }
    }

    let series = [{
      name: 'Cholesterol',
      data: graphData.cholesterol
    }]

    return (
       loading ? <h1> loading... </h1> :
      <div id="chart">
      <Chart options={options} series={series} type="bar" height={350} />
      <table class="table table-hover">
        <thead class="thead-dark">
          <tr>
            <th scope="col">High Cholesterol Count</th>
            <th scope="col">High Systolic Count</th>
            <th scope="col">High Diastolic Count</th>
            <th scope="col">Non-Smoker Count</th>
          </tr>
        </thead>
        <tbody>
          {/* {listItems} */}
          <tr >
            <td>{cholCount}</td>
            <td>{sysCount}</td>
            <td>{diaCount}</td>
            <td>{smokerCount}</td>
          </tr>
          </tbody>
      </table>
    </div>

    );
  };



  export default CholestrolGraph