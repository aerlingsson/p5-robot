using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace ColourScript {
        public class ColorScript : MonoBehaviour 
    {
        // If public, then it's available/visible in the inspector in unity.
        Material[] materials;
        Material[] mats;
        Color[] colors = { Color.yellow, Color.cyan, Color.red, Color.green, Color.blue, Color.magenta, Color.gray };
        Renderer rend;
        public Shader shader;
        Material randMat;

        // Start is called before the first frame update
        void Start () {
            // Make a render component to rend stuff in-game.
            rend = GetComponent<Renderer> ();
            rend.enabled = true;

            // Loads all materials from the folder "Materialss" important that there are two s's or it will take other Material folders.
            mats = Resources.LoadAll ("BackgroundMaterials", typeof (Material)).Cast<Material> ().ToArray ();


            // Add a bunch of colors to an array from where we can pick a random one.
            ChangeColourAndMaterial();

        }

        public void ChangeColourAndMaterial () {
            randMat = mats[Random.Range (0, mats.Length)];
            rend.sharedMaterial = randMat; // Apply the material to the plane object.
            rend.material.shader = shader; // Apply shader to the plane object.

            Color col = colors[(Random.Range (0, colors.Length))];
            rend.material.color = col; // Apply the color to the plane object.

            foreach (Transform child in transform) {
                child.GetComponent<Renderer> ().material = randMat; // Apply material to the child.
                child.GetComponent<Renderer> ().material.color = col; // Apply the color to the child.
                child.GetComponent<Renderer> ().material.shader = shader; // Apply the shader to the child.
            }
        }

    }
}