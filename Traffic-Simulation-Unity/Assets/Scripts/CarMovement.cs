using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarMovement : MonoBehaviour
{

    [SerializeField] Vector3 startPos;
    [SerializeField] Vector3 stopPos;
    [SerializeField] float motionTime;

    float currentTime;
    float t;



    float getT(){
        currentTime += Time.deltaTime;
        t = currentTime/motionTime;
        if(t>1){
            t = 1;
        }
        return t;
    }

    void RandomPoints(){
        t = getT();
        transform.position = Vector3.Lerp(startPos, stopPos, t);

        if(t==1){
            currentTime = 0;
            startPos = stopPos;
            Vector2 displacement = Random.insideUnitCircle * 5;
            stopPos = new Vector3(startPos.x + displacement.x, 0, startPos.z + displacement.y);
        }
    }


    void SimpleMotion() {
        transform.position = Vector3.Lerp(startPos, stopPos, getT());
    }
    
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        // SimpleMotion();
        RandomPoints();
    }
}
