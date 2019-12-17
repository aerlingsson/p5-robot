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
    public float _motorForce = 0.16f;
    int _allowedToDrive = 0;
    float _steerangl = 0.0f;
    float turningNumber = 0.0f;

    // load into arrays all gameobjects with "spawnpoint" and "SpotLight" as tags
    void Awake () {
        spawnlocations = GameObject.FindGameObjectsWithTag ("spawnpoint");
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
        back_driver_col.motorTorque = _motorForce * _allowedToDrive;
        back_passenger_col.motorTorque = _motorForce * _allowedToDrive;
    }

    //Resets the car and progressTracker. Randomize the lights, material and colour of said material on each reset
    // also locks the movement of the car through allowedToDrive
    public override void AgentReset () {
        float intensityR = 0f;
        int spawn = Random.Range (0, spawnlocations.Length);
        int Rot = Random.Range (0, 2);

        foreach (GameObject light in lights) {
            if (Random.Range (0, 2) == 0) {
                light.SetActive (false);

            } else {
                //float LightRotation = Random.Range(0.0f, 10.0f);
                intensityR = Random.Range (0.2f, 1.0f);
                light.SetActive (true);
                light.GetComponent<Light> ().intensity = intensityR;
                light.GetComponent<Light> ().spotAngle = Random.Range (10, 90);
                //light.transform.rotation = Quaternion.Euler(new Vector3(90,90,90));
                //light.transform.rotation *= Quaternion.Euler(new Vector3(LightRotation,1,1));

            }
        }
        colourScript.ChangeColourAndMaterial ();
        this.rBody.angularVelocity = Vector3.zero;
        this.rBody.velocity = Vector3.zero;
        intensityR = Random.Range (0.2f, 1.0f);
        directionalLight.GetComponent<Light> ().intensity = intensityR;
        this.transform.position = spawnlocations[spawn].transform.position;
        this.transform.rotation = spawnlocations[spawn].transform.rotation * Quaternion.Euler (new Vector3 (0, (180f * Rot), 0));
        _allowedToDrive = 0;
        progressTracker.Reset ();

    }

    public override void CollectObservations () {

    }

    public void turnCar (float[] act) {
        var action = Mathf.FloorToInt (act[0]);
        switch (action) {
            case 1:
                _steerangl = 21.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 22.0f;
                break;

            case 2:
                _steerangl = 18.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 18.0f;
                break;

            case 3:
                _steerangl = 12.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 12.0f;
                break;

            case 4:
                _steerangl = 6.0f;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 6.0f;
                break;

            case 5:
                _steerangl = _steerangl - turningNumber;
                front_driver_col.steerAngle = _steerangl;
                front_passenger_col.steerAngle = _steerangl;
                turningNumber = 0;
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
                turningNumber = -22.0f;
                break;

        }

    }
    public override void AgentAction (float[] vectorAction, string textAction) {
        turnCar (vectorAction);

        //Locks movement and rewards until the progressTracker target is in place near the car
        if (progressTracker.SetupDone () == true) {
            _allowedToDrive = 1;
            SetReward (1.0f - progressTracker.getDistanceFromCenter ());
        }

    }

    //resets if car drives off of the track
    void OnCollisionEnter (Collision collision) {
        if (collision.collider.tag == "plane") {
            SetReward (-10.0f);
            Done ();
        }
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
