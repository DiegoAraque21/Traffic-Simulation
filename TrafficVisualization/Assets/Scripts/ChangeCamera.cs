using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChangeCamera : MonoBehaviour
{

    // Cameras
    public GameObject cam1;
    public GameObject cam2;
    public GameObject cam3;
    public GameObject cam4;
    public GameObject cam5;
    int nCameras = 5;
    int counter = 1;

    // Update is called once per frame
    void Update()
    {
        // On press space
        if (Input.GetButtonDown("Jump"))
        {
            // Change camera view
            cam1.SetActive(counter % nCameras == 0);
            cam2.SetActive(counter % nCameras == 1);
            cam3.SetActive(counter % nCameras == 2);
            cam4.SetActive(counter % nCameras == 3);
            cam5.SetActive(counter % nCameras == 4);
            counter++;
        }
    }
}
