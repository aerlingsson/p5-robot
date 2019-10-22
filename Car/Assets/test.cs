using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class test : MonoBehaviour
{
    
    // Start is called before the first frame update
public Vector2 textureSize;
private Material wallMaterial;

// Update is called once per frame
void Update() //or Start, if you don't need realtime rescaling.
{
    GetComponent<Renderer>().materials[0].mainTextureScale = new Vector2(transform.localScale.x / textureSize.x, transform.localScale.y / textureSize.y);
    GetComponent<Renderer>().materials[1].mainTextureScale = new Vector2(transform.localScale.x / textureSize.x, transform.localScale.z / textureSize.y);
    GetComponent<Renderer>().materials[2].mainTextureScale = new Vector2(transform.localScale.z / textureSize.x, transform.localScale.y / textureSize.y);
}
}
