using UnityEngine;

namespace PathCreation.Examples {
    // Example of creating a path at runtime from a set of points.

    [RequireComponent(typeof(PathCreator))]
    public class GeneratePathExample : MonoBehaviour {

        public bool closedLoop = false;
        public Transform[] waypoints;

        void Start () {
            if (waypoints.Length > 0) {
                // Create a new bezier path from the waypoints.
                foreach (Transform t in waypoints)
                {
                    float zRange = Random.Range (0.0f, 3.0f);
                    int front = Random.Range(0, 2);
                    if(front == 0){
                    t.position = t.position + new Vector3(0,0,zRange);
                    }else
                    {
                        t.position = t.position - new Vector3(0,0,zRange);
                    }
                }
                BezierPath bezierPath = new BezierPath (waypoints, closedLoop, PathSpace.xyz);
                GetComponent<PathCreator> ().bezierPath = bezierPath;
            }
        }
    }
}