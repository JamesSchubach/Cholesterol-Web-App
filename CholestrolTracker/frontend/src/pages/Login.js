import React, { useState, useEffect } from "react";
import axios from "axios";
import { Modal, Button, Form } from "react-bootstrap";


const Login = (props) => {
    const [error, setError] = useState('')
    const [id, setId] = useState('sup')
    const url = window.location.origin

    const validateData= async (e, id) =>{
        e.preventDefault()
        let result 
        try{
            result = await axios(url+ "/api/practitioner/" + id);
        }
        catch {
            setError('invalid id: ' + id)
        }
            props.history.push({
                pathname: '/dashboard/'+id +'/',
            })
    }
    
    return (
        <div>
            <div className="row align-items-center h-100">
                <div className="card text-center mx-auto mh-50" style={{width: '18rem'}}>
                    <div className="card-body">
                        <h5 className="card-title">Sign In</h5>
                        <Form onSubmit={(e)=>{validateData(e, id)}}>
                            <Form.Group controlId="formBasicEmail">
                                <Form.Label>Practitioner ID</Form.Label>
                                <Form.Control type="input" placeholder="Enter your ID Number" onChange={(e)=>{setId(e.target.value)}}/>
                            </Form.Group>
                            <Button variant="primary" type="submit">
                                Submit
                            </Button>
                            </Form>
                        <p style={{color: 'red'}}> {error} </p>
                    </div>
                </div>
            </div>
        </div> );
};

export default Login;
