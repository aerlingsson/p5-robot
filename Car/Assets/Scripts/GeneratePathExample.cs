using UnityEngine;

namespace PathCreation.Examples {
    // Example of creating a path at runtime from a set of points.

    [RequireComponent (typeof (PathCreator))]
    public class GeneratePathExample : MonoBehaviour {

        public bool closedLoop = false;
        public Transform[] waypoints;
        public Transform car;
        public Transform target;
        public PathCreator pathcreator;
        public Transform[] ControlWaypoints;

        void Start () {
            GeneratePath ();
        }

        void Update () {
            if (pathcreator != null) {
                target.position = pathcreator.path.GetClosestPointOnPath (car.position) + new Vector3 (0f, 0.0625f, 0f);
            }
        }

        public void GeneratePath () {
            if (waypoints.Length > 0) {
                // Create a new bezier path from the waypoints.
                reset ();
                foreach (Transform t in waypoints) {
                    if (!(t.CompareTag ("Start") || t.CompareTag("Start2")|| t.CompareTag ("goal"))) {
                        float zRange = Random.Range (0.0f, 0.4f);
                        int front = Random.Range (0, 2);
                        if (front == 0) {
                            t.position = t.position + new Vector3 (0, 0, zRange);
                        } else {
                            t.position = t.position - new Vector3 (0, 0, zRange);
                        }
                    }
                }
                BezierPath bezierPath = new BezierPath (waypoints, closedLoop, PathSpace.xyz);
                pathcreator.bezierPath = bezierPath;
            }
        }

        public float getNormalizedDistanceFromCenter () {
            float distance = Vector3.Distance (car.position, target.position);
            float distanceNormalized = Mathf.InverseLerp (0.0f, 0.3f, distance);
            Debug.Log(distanceNormalized);
            return distanceNormalized;
        }

        public void reset () {
            for (int i = 0; i < ControlWaypoints.Length; i++) {
                waypoints[i].position = ControlWaypoints[i].position;
            }
        }

        public bool setup () {
            float distanceCheck = Vector3.Distance (car.position, GameObject.FindWithTag ("Start").transform.position);
            bool done;
            if (distanceCheck > 0.3f) {
                done = true;
            } else {
                done = false;
            }
            return done;
        }
        void OnDrawGizmos () {
            if (Application.isPlaying) {
                Gizmos.color = Color.green;
                Gizmos.DrawLine (car.position, target.position);
            }
        }

    }
}