using System.Collections;
using System.Collections.Generic;
using ColourScript;
using MLAgents;
using PathCreation.Examples;
using UnityEngine;
using UnityStandardAssets.Utility;
public class carAgentV2 : Agent {
    Rigidbody rBody;
    public GeneratePathExample pathcreator;
    public RoadMeshCreator meshcreator;
    public ColorScript colourScript;
    private GameObject[] lights;
    public GameObject directionalLight;
    public Transform[] waypoints;
    public Transform spawn;
    public WheelCollider front_driver_col, front_passenger_col;
    public WheelCollider back_driver_col, back_passenger_col;
    public Transform frontDriver, frontPassenger;
    public Transform backDriver, backPassenger;
    Transform startPos;
    public float _motorForce = 0.16f;
    float _steerangl = 0.0f;
    float turningNumber = 0.0f;

    // load into arrays all gameobjects with "spawnpoint" and "SpotLight" as tags
    void Awake () {
        lights = GameObject.FindGameObjectsWithTag ("SpotLight");
    }

    // initialize the rigid body
    void Start () {
        rBody = GetComponent<Rigidbody> ();
    }

    // Update the position of the cyliders to match the position and rotation of the colliders to provide animation
    // and set the motortorque so that the car moves
    void FixedUpdate () {
        updateWheelPos (front_driver_col, frontDriver);
        updateWheelPos (front_passenger_col, frontPassenger);
        updateWheelPos (back_driver_col, backDriver);
        updateWheelPos (back_passenger_col, backPassenger);
        back_driver_col.motorTorque = _motorForce;
        back_passenger_col.motorTorque = _motorForce;
    }

    //Resets the car and progressTracker. Randomize the lights, material and colour of said material on each reset
    public override void AgentReset () {
        float intensityR = 0f;
        pathcreator.GeneratePath ();
        meshcreator.creation ();
        colourScript.ChangeColourAndMaterial ();
        this.rBody.angularVelocity = Vector3.zero;
        this.rBody.velocity = Vector3.zero;
        intensityR = Random.Range (0.2f, 1.0f);
        directionalLight.GetComponent<Light> ().intensity = intensityR;
 
        this.transform.position = spawn.position;
        this.transform.rotation = spawn.rotation;
        foreach (GameObject light in lights) {
            if (Random.Range (0, 2) == 0) {
                light.SetActive (false);

            } else {
                intensityR = Random.Range (0.2f, 3.0f);
                int waypointsR = Random.Range(0, waypoints.Length);
                light.SetActive (true);
                light.GetComponent<Light> ().intensity = intensityR;
                light.GetComponent<Light>().transform.LookAt(waypoints[waypointsR]);
                light.GetComponent<Light> ().spotAngle = Random.Range (10, 90);

            }
        }

    }

    public override void CollectObservations () {

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
                _steerangl = 22.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 22.0f;
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
                _steerangl = 6.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 6.0f;
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
                _steerangl = -22.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = -22.0f;
                break;

        }

    }
    public override void AgentAction (float[] vectorAction, string textAction) {
        turnCar (vectorAction);

        if(pathcreator.getNormalizedDistanceFromCenter() < 0.33f ){
        SetReward (1.0f - (3 * pathcreator.getNormalizedDistanceFromCenter ()));
        }
        else if (pathcreator.getNormalizedDistanceFromCenter() >= 0.33f){
            SetReward(-1.0f);
        }
        
        if (pathcreator.setup ()) {
            if (pathcreator.getNormalizedDistanceFromCenter () >= 1) {
                SetReward (-10.0f);
                Done ();
            }
        }

    }

    void OnCollisionEnter (Collision collision) {
        if (collision.collider.tag == "Finish") {
            SetReward (10.0f);
            Done ();
        }
    }

    private void OnTriggerEnter (Collider other) {

    }

    //Sets the position of the transform equal to the postion of the collider
    void updateWheelPos (WheelCollider col, Transform t) {
        Vector3 pos = t.position;
        Quaternion rot = t.rotation;

        col.GetWorldPose (out pos, out rot);
        t.position = pos;
        rot = rot * Quaternion.Euler (new Vector3 (0, 0, 90));
        t.rotation = rot;

    }

}
