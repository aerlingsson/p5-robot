using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarControl : MonoBehaviour
{

    public WheelCollider front_driver_col, front_passenger_col;
    public WheelCollider back_driver_col, back_passenger_col;


    public Transform frontDriver, frontPassenger;
    public Transform backDriver, backPassenger;

    public float _steerAngle = 30.0f;
    public float _motorForce = 100f;
    public float steerAngl;
    float h,v;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        Inputs();
        Drive();
        SteerCar();

        updateWheelPos(front_driver_col, frontDriver);
        updateWheelPos(front_passenger_col, frontPassenger);
        updateWheelPos(back_driver_col, backDriver);
        updateWheelPos(back_passenger_col, backPassenger);
    }

    void Inputs()
    {
        h = Input.GetAxis("Horizontal");
        v = Input.GetAxis("Vertical");
    }

    void Drive()
    {
        
        back_driver_col.motorTorque = v * _motorForce;
        back_passenger_col.motorTorque = v * _motorForce;

    }

    void SteerCar()
    {
        steerAngl = _steerAngle * h;
        front_driver_col.steerAngle = steerAngl;
        front_passenger_col.steerAngle = steerAngl;
    }

    void updateWheelPos(WheelCollider col, Transform t)
    {
        Vector3 pos = t.position;
        Quaternion rot = t.rotation;

        col.GetWorldPose(out pos, out rot);
        t.position = pos;
        rot = rot * Quaternion.Euler(new Vector3(0, 0, 90));
        t.rotation = rot;

    }
}
