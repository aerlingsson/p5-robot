using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class ColorScript : MonoBehaviour
{
    // If public, then it's available/visible in the inspector in unity.
    Material[] materials;
    Color[] colors;
    Renderer rend;
    public Shader shader;

    // Start is called before the first frame update
    void Start()
    {
        // Make a render component to rend stuff in-game.
        rend = GetComponent<Renderer>();
        rend.enabled = true;

        // Loads all materials from the folder "Materialss" important that there are two s's or it will take other Material folders.
        Material[] mats = Resources.LoadAll("BackgroundMaterials", typeof(Material)).Cast<Material>().ToArray();
        Material randMat = mats[Random.Range(0, mats.Length)];
        rend.sharedMaterial = randMat; // Apply the material to the plane object.
        rend.material.shader = shader; // Apply shader to the plane object.
        
        // Add a bunch of colors to an array from where we can pick a random one.
        Color[] colors = { Color.yellow, Color.cyan, Color.red, Color.green, Color.blue, Color.magenta, Color.gray};
        Color col = colors[(Random.Range(0, colors.Length))];
        rend.material.color = col; // Apply the color to the plane object.

        foreach (Transform child in transform) {
            child.GetComponent<Renderer>().material = randMat; // Apply material to the child.
            child.GetComponent<Renderer>().material.color = col; // Apply the color to the child.
            child.GetComponent<Renderer>().material.shader = shader; // Apply the shader to the child.
        }


    }

}
