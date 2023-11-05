using System.Collections;
using System.Collections.Generic;
using UnityEngine.SceneManagement;
using UnityEngine;

public class MAD_SceneLoader : MonoBehaviour
{
    public void NextScene()
    {
        SceneManager.LoadScene("MAD_Cubemos");
    }
}
