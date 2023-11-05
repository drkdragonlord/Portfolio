using UnityEngine;
using System.Collections;
using System;
using UnityEngine.SceneManagement;
//using System.Runtime.Serialization.Formatters.Binary;
//using System.Runtime.Serialization.Formatters.Binary;
using System.IO;

public class MAD_DataManager : MonoBehaviour
{
    public static MAD_DataManager instance = null;

    void Awake()
    {
        //Create one instance of object and make persistant.
        if (instance == null)
        {
            instance = this;
            //PlayerPrefs.DeleteAll();
        }
        else if (instance != this)
        {
            Destroy(gameObject);
        }
        DontDestroyOnLoad(gameObject);
    }

    void Start() 
    { 
    }
    void Update() 
    { 
    }

    public static void SaveData(string name, float x, float y, float z, float rotX, float rotY, float rotZ, float currentTime)
    {

    }
}
