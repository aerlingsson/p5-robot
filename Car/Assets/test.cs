using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class test : MonoBehaviour {

    public Rigidbody car;
    public WheelCollider fl,fr,hl,hr;
    public float motorMax = 300, steerMax = 60;

    // Use this for initialization
    void Start () {

    }
	
	void Update () {
        float motor = - Input.GetAxis("Vertical");
        float steer = Input.GetAxis("Horizontal") * steerMax;
        hl.motorTorque = motor * motorMax;
        hr.motorTorque = motor * motorMax;
        Vector3 position;
        Quaternion rotation;
        
        fl.steerAngle = steer;
        fr.steerAngle = steer;
        fl.GetWorldPose(out position, out rotation);
        fl.transform.rotation = rotation;
        fr.transform.rotation = rotation;
        hr.GetWorldPose(out position, out rotation);
        hl.transform.rotation = rotation;
        hr.transform.rotation = rotation;
        Debug.Log(car.velocity);
    }
}
