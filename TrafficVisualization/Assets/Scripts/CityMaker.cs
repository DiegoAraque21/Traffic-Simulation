using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CityMaker : MonoBehaviour
{
    [SerializeField] TextAsset layout;
    [SerializeField] GameObject roadPrefab;
    [SerializeField] GameObject buildingPrefab;
    [SerializeField] GameObject building2Prefab;
    [SerializeField] GameObject building3Prefab;
    [SerializeField] GameObject fountainPrefab;
    [SerializeField] GameObject lampPrefab;
    [SerializeField] GameObject semaphorePrefab;
    [SerializeField] GameObject semaphoreRedPrefab;
    [SerializeField] GameObject car1;
    [SerializeField] GameObject car2;
    [SerializeField] GameObject car3;
    [SerializeField] GameObject car4;
    [SerializeField] int tileSize;

    // Start is called before the first frame update
    void Start()
    {
        MakeTiles(layout.text);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void MakeTiles(string tiles)
    {
        int x = 0;
        // Mesa has y 0 at the bottom
        // To draw from the top, find the rows of the file
        // and move down
        // Remove the last enter, and one more to start at 0
        int y = tiles.Split('\n').Length - 2;

        Vector3 position;
        GameObject tile;

        for (int i=0; i<tiles.Length; i++) { 
            if (tiles[i] == '>' || tiles[i] == '<') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'v' || tiles[i] == '^') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'L' || tiles[i] == 'R') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'U' || tiles[i] == 'A') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'D') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(buildingPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.GetComponent<Renderer>().materials[0].color = Color.green;
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '#') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                // random number between 0 and 1
                float r = Random.value;
                if (r < 0.20) {
                    tile = Instantiate(buildingPrefab, position, Quaternion.identity);
                } else if (r < 0.70) {
                    tile = Instantiate(building2Prefab, position, Quaternion.identity);
                } else {
                    tile = Instantiate(building3Prefab, position, Quaternion.identity);
                }
                tile.transform.localScale = new Vector3(1, Random.Range(0.6f, 3.0f), 1);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'F'){
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(fountainPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'G'){
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(lampPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '\n') {
                x = 0;
                y -= 1;
            }
        }

    }
}
