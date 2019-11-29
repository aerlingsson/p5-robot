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
    private GameObject[] spawnlocations;
    private GameObject[] lights;
    public GameObject directionalLight;
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
        lights = GameObject.FindGameObjectsWithTag("SpotLight");
    }

    void Start () {
        rBody = GetComponent<Rigidbody> ();
    }

    void FixedUpdate () {
        updateWheelPos (front_driver_col, frontDriver);
        updateWheelPos (front_passenger_col, frontPassenger);
        updateWheelPos (back_driver_col, backDriver);
        updateWheelPos (back_passenger_col, backPassenger);
        back_driver_col.motorTorque = _motorForce;
        back_passenger_col.motorTorque = _motorForce;
    }

    public override void AgentReset () {
        float intensityR = 0f;
        int spawn = Random.Range (0, spawnlocations.Length);
        int Rot = Random.Range(0,2);

        foreach(GameObject light in lights)
         {
            if(Random.Range(0,2) == 0){
                light.SetActive(false);

            }
            else {
                //float LightRotation = Random.Range(0.0f, 10.0f);
                intensityR = Random.Range(0.2f, 1.0f);
                light.SetActive(true);
                light.GetComponent<Light>().intensity = intensityR;
                light.GetComponent<Light>().spotAngle = Random.Range(10, 90);
                //light.transform.rotation = Quaternion.Euler(new Vector3(90,90,90));
                //light.transform.rotation *= Quaternion.Euler(new Vector3(LightRotation,1,1));

            
            }
         }
        colourScript.ChangeColourAndMaterial ();
        this.rBody.angularVelocity = Vector3.zero;
        this.rBody.velocity = Vector3.zero;
        intensityR = Random.Range(0.2f, 1.0f);
        directionalLight.GetComponent<Light>().intensity = intensityR;
        this.transform.position = spawnlocations[spawn].transform.position;
        this.transform.rotation = spawnlocations[spawn].transform.rotation * Quaternion.Euler(new Vector3(0,(180f * Rot),0));
        _motorForce = 0.0f;
        progressTracker.Reset ();

    }

    public override void CollectObservations () {

    }

    public void turnCar (float[] act) {
        var action = Mathf.FloorToInt (act[0]);
        Debug.Log(action);
        switch (action) {
            case 1:
                _steerangl = _steerangl - turningNumber;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 0;
                break;

            case 2:
                _steerangl = 6.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 6.0f;
                break;

            case 3:
                _steerangl = 12.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 12.0f;
                break;

            case 4:
                _steerangl = 18.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 18.0f;
                break;

            case 5:
                _steerangl = 21.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 21.0f;
                break;

            case 6:
                _steerangl = -6.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = -6.0f;
                break;

            case 7:
                _steerangl = -12.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = -12.0f;
                break;

            case 8:
                _steerangl = -18.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = -18.0f;
                break;

            case 9:
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
            SetReward (1.0f - progressTracker.getDistanceFromCenter ());
        }


    }

    void OnCollisionEnter (Collision collision) {
        if(collision.collider.tag == "plane"){
            SetReward(-10.0f);
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