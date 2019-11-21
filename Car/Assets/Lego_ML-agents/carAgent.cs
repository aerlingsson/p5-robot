using System.Collections;
using System.Collections.Generic;
using ColourScript;
using MLAgents;
using UnityEngine;
using UnityStandardAssets.Utility;
public class carAgent : Agent {
    Rigidbody rBody;
    public WaypointProgressTracker progressTracker; // A reference to the waypoint-based route we should follow
    public ColorScript colourScript;
    [HideInInspector] public GameObject[] spawnlocations;
    public WheelCollider front_driver_col, front_passenger_col;
    public WheelCollider back_driver_col, back_passenger_col;
    public Transform frontDriver, frontPassenger;
    public Transform backDriver, backPassenger;
    float _steerAngle = 30.0f;
    float _motorForce = 0.0f;
    float _steerangl = 0.0f;
    float turningNumber = 0.0f;

    void Awake () {
        spawnlocations = GameObject.FindGameObjectsWithTag ("spawnpoint");
    }

    void Start () {
        rBody = GetComponent<Rigidbody> ();
        //startPos = transform.position;
        //startRot = transform.eulerAngles;

    }

    // Update is called once per frame
    void FixedUpdate () {
        updateWheelPos (front_driver_col, frontDriver);
        updateWheelPos (front_passenger_col, frontPassenger);
        updateWheelPos (back_driver_col, backDriver);
        updateWheelPos (back_passenger_col, backPassenger);
        back_driver_col.motorTorque = _motorForce;
        back_passenger_col.motorTorque = _motorForce;
    }

    public override void AgentReset () {
        colourScript.ChangeColourAndMaterial ();
        this.rBody.angularVelocity = Vector3.zero;
        this.rBody.velocity = Vector3.zero;
        //transform.position = startPos;
        //transform.eulerAngles = startRot;
        /*this.transform.position = new Vector3(5.133f, 0.14f, 16.752f);
        this.transform.rotation = Quaternion.Euler(new Vector3(0.0f, 0.0f, 0.0f));*/
        int spawn = Random.Range (0, spawnlocations.Length);
        this.transform.position = spawnlocations[spawn].transform.position;
        _motorForce = 0.0f;
        progressTracker.Reset ();

    }

    public override void CollectObservations () {
        //position of the agent used for rewards
        //AddVectorObs(this.transform.position);
        //wheelcolliders used to driver and steer the agent
        //AddVectorObs(back_driver_col.motorTorque);
        //AddVectorObs(back_passenger_col.motorTorque);
        //AddVectorObs(front_driver_col.steerAngle);
        //AddVectorObs(front_passenger_col.steerAngle);
    }

    public void turnCar (float[] act) {
        var action = Mathf.FloorToInt (act[0]);

        switch (action) {
            case 0:
                _steerangl = _steerangl - turningNumber;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 0;
                break;

            case 1:
                _steerangl = 6.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 6.0f;
                break;

            case 2:
                _steerangl = 12.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 12.0f;
                break;

            case 3:
                _steerangl = 18.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 18.0f;
                break;

            case 4:
                _steerangl = 21.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 21.0f;
                break;

            case 5:
                _steerangl = -6.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = -6.0f;
                break;

            case 6:
                _steerangl = -12.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = -12.0f;
                break;

            case 7:
                _steerangl = -18.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = -18.0f;
                break;

            case 8:
                _steerangl = -21.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = -21.0f;
                break;

        }

    }
    public override void AgentAction (float[] vectorAction, string textAction) {
        turnCar (vectorAction);
        /*
        //Actions, size = 2
        Vector3 controlSignal = Vector3.zero;
        controlSignal.x = vectorAction[0];
       //controlSignal.z = vectorAction[1];
        //back_driver_col.motorTorque = (controlSignal.z * _motorForce);
        //back_passenger_col.motorTorque = (controlSignal.z * _motorForce);
        front_driver_col.steerAngle = (controlSignal.x * _steerAngle);
        front_passenger_col.steerAngle = (controlSignal.x * _steerAngle);

        //rewards
        if(controlSignal.z <= 0 || controlSignal.z <= 0){
            SetReward(-0.5f);
        }
        else if (controlSignal.z > 0 || controlSignal.z > 0){
            SetReward(0.1f);
        }
        */

        if (progressTracker.SetupDone () == true) {
            _motorForce = 300.0f;

            //if (progressTracker.getDistanceFromCenter() >= 1)
            //{
            //  SetReward(-1.0f);
            //Done();
            //}
        }

        SetReward (1.0f - progressTracker.getDistanceFromCenter ());

    }

    void OnCollisionEnter (Collision collision) {
        if(collision.collider.tag == "plane"){
            Done();
        }
    }

    
    void updateWheelPos (WheelCollider col, Transform t) {
        Vector3 pos = t.position;
        Quaternion rot = t.rotation;

        col.GetWorldPose (out pos, out rot);
        t.position = pos;
        rot = rot * Quaternion.Euler (new Vector3 (0, 0, 90));
        t.rotation = rot;

    }
}