using System.Collections;
using System.Collections.Generic;
using UnityEngine.SceneManagement;
using UnityEngine;

public class MAD_SceneLoader : MonoBehaviour
{
    public void RoutineSelection()
    {
        SceneManager.LoadScene("MAD_RoutineSelect");
    }
    public void SquatRoutine()
    {
        SceneManager.LoadScene("MAD_SquatRoutine");
    }

    public void LungesRoutine()
    {
        SceneManager.LoadScene("MAD_LungesRoutine");
    }

    public void RandomRoutine()
    {
        SceneManager.LoadScene("MAD_RandomRoutine");
    }

    public void ArmsRaiseRoutine()
    {
        SceneManager.LoadScene("MAD_ArmsRaiseRoutine");
    }
}
