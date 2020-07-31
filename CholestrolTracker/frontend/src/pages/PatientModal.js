import React, { useState, useEffect } from "react";
import axios from "axios";
import { Modal, Button, Form, Dropdown } from "react-bootstrap";
import {patientController, practitionerController} from '../views/View';
import Chart from "react-apexcharts";


const PatientModal = (props) => {
    const handleClose = () => props.setShow(false);
    const handleShow = () => props.setShow(true);

    return (
      <>
        <Modal show={props.show} onHide={handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>{props.patient.given_name} {props.patient.family_name}</Modal.Title>
          </Modal.Header>
          <Modal.Body>Full Name: {props.patient.prefix_name} {props.patient.given_name} {props.patient.family_name}</Modal.Body>
          <Modal.Body>DOB: {props.patient.birth_date}</Modal.Body>
          <Modal.Body>Gender: {props.patient.gender}</Modal.Body>
          <Modal.Body>City: {props.patient.city}</Modal.Body>
          <Modal.Body>State: {props.patient.state}</Modal.Body>
          <Modal.Body>Country: {props.patient.country}</Modal.Body>
          <BloodGraph patient={props.patient.graph} />
        </Modal>
      </>
    );
  };

  const BloodGraph = (props) =>{
    let seriesData = []
    let categoryData = []

    if (props.patient.length > 0){
      seriesData = props.patient.map((item)=>{return item[0]})
      seriesData = seriesData.filter(Number)
  
      categoryData = seriesData.map((item, index)=>{
        return index
      })
    }

    let series =  [{
      name: "Blood Pressure",
      data: seriesData
    }]

    let options = {
      chart: {
        height: 350,
        type: 'line',
        zoom: {
          enabled: false
        }
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        curve: 'straight'
      },
      title: {
        text: 'Blood Test History',
        align: 'left'
      },
      grid: {
        row: {
          colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
          opacity: 0.5
        },
      },
      xaxis: {
        categories: categoryData,
      }
    }

    return (
      <div id="chart">
    <Chart options={options} series={series} type="line" height={350} />
     </div> 
     )
  }

  export default PatientModal;