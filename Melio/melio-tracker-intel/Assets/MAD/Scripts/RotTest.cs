using System.Collections;
using System.Collections.Generic;
using System.Text;
using UnityEngine;
using UnityEngine.UI;

public class RotTest : MonoBehaviour
{
    [SerializeField]
    public GameObject object1;
    public GameObject object2;    

    [SerializeField]
    public float repeatRate = 0.1f;

    [SerializeField]
    public float time = 0.1f;

    [SerializeField]
    public Quaternion object01Rotation;

    [SerializeField]
    public GameObject TestArm;

    [SerializeField]
    public Transform TestArmRoot;

    [SerializeField]
    public GameObject MercyRig;

    [SerializeField]
    public Transform MercyHips;

    [SerializeField]
    private Transform[] MercyJoints;

    [SerializeField]
    public Transform[] UsableMercyJoints;

    [SerializeField]
    public Text DirData;

    [SerializeField]
    public Text RotData;

    [SerializeField]
    public Text LookData;

    private enum FollowBehavior { Forward, Up, Right}

    [SerializeField]
    private FollowBehavior follow;
    // Start is called before the first frame update
    void Start()
    {
        object1 = Instantiate(object1, new Vector3(0.2f,0, 0), UnityEngine.Quaternion.identity) as GameObject;
        object2 = Instantiate(object2, new Vector3(0.5f,0, 0), UnityEngine.Quaternion.identity) as GameObject;
        TestArm = Instantiate(TestArm, new Vector3(0, 0, 0), UnityEngine.Quaternion.identity) as GameObject;
        MercyRig = Instantiate(MercyRig, new Vector3(0, 0, 0), UnityEngine.Quaternion.identity) as GameObject;

        object1.name = "RotationSource";
        object2.name = "RotationAimVector";

        object1.transform.localScale = new Vector3(0.1f, 0.1f, 0.1f);
        object2.transform.localScale = new Vector3(0.1f, 0.1f, 0.1f);

        //MercyHips = MercyRig.transform.GetChild(8);
        MercyHips = MercyRig.transform.GetChild(2);

        TestArmRoot = TestArm.transform.GetChild(0);
        Debug.Log(TestArmRoot.name);

        MercyJoints = MercyHips.GetComponentsInChildren<Transform>();
        UsableMercyJoints = new Transform[20];
        for (int i = 0; i < 20; i++)
        {
            if (i == 0)
            {
                UsableMercyJoints[i] = MercyJoints[39];
            }
            //neck
            if (i == 1)
            {
                UsableMercyJoints[i] = MercyJoints[38];
            }
            //right shoulder
            if (i == 2)
            {
                UsableMercyJoints[i] = MercyJoints[44];
            }
            //right elbow
            if (i == 3)
            {
                UsableMercyJoints[i] = MercyJoints[45];
            }
            //right hand
            if (i == 4)
            {
                UsableMercyJoints[i] = MercyJoints[46];
            }
            //left shoulder
            if (i == 5)
            {
                UsableMercyJoints[i] = MercyJoints[15];
            }
            //left elbow
            if (i == 6)
            {
                UsableMercyJoints[i] = MercyJoints[16];
            }
            //left hand
            if (i == 7)
            {
                UsableMercyJoints[i] = MercyJoints[17];
            }
            //right Thigh
            if (i == 8)
            {
                UsableMercyJoints[i] = MercyJoints[6];
            }
            //right Knee
            if (i == 9)
            {
                UsableMercyJoints[i] = MercyJoints[7];
            }
            //right Ankle
            if (i == 10)
            {
                UsableMercyJoints[i] = MercyJoints[8];
            }
            //left Thigh
            if (i == 11)
            {
                UsableMercyJoints[i] = MercyJoints[1];
            }
            //left Knee
            if (i == 12)
            {
                UsableMercyJoints[i] = MercyJoints[2];
            }
            //left Ankle
            if (i == 13)
            {
                UsableMercyJoints[i] = MercyJoints[3];
            }
            //right eye
            if (i == 14)
            {
                UsableMercyJoints[i] = MercyJoints[42];
            }
            //left eye
            if (i == 15)
            {
                UsableMercyJoints[i] = MercyJoints[41];
            }
            //hips
            if (i == 16)
            {
                UsableMercyJoints[i] = MercyJoints[0];
            }
            //spine1
            if (i == 17)
            {
                UsableMercyJoints[i] = MercyJoints[11];
            }
            //spine2
            if (i == 18)
            {
                UsableMercyJoints[i] = MercyJoints[12];
            }
            //spine3
            if (i == 19)
            {
                UsableMercyJoints[i] = MercyJoints[13];
            }
        }
            //Mercy Joints Short Listing
            /*
            UsableMercyJoints = new Transform[20];
            for (int i = 0; i < 20; i++)
            {
                if (i == 0)
                {
                    UsableMercyJoints[i] = MercyJoints[68].transform;
                }
                if (i == 1)
                {
                    UsableMercyJoints[i] = MercyJoints[65].transform;
                }
                if (i == 2)
                {
                    UsableMercyJoints[i] = MercyJoints[41].transform;
                }
                if (i == 3)
                {
                    UsableMercyJoints[i] = MercyJoints[42].transform;
                }
                if (i == 4)
                {
                    UsableMercyJoints[i] = MercyJoints[43].transform;
                }
                if (i == 5)
                {
                    UsableMercyJoints[i] = MercyJoints[16].transform;
                }
                if (i == 6)
                {
                    UsableMercyJoints[i] = MercyJoints[17].transform;
                }
                if (i == 7)
                {
                    UsableMercyJoints[i] = MercyJoints[18].transform;
                }
                if (i == 8)
                {
                    UsableMercyJoints[i] = MercyJoints[6].transform;
                }
                if (i == 9)
                {
                    UsableMercyJoints[i] = MercyJoints[7].transform;
                }
                if (i == 10)
                {
                    UsableMercyJoints[i] = MercyJoints[8].transform;
                }
                if (i == 11)
                {
                    UsableMercyJoints[i] = MercyJoints[9].transform;
                }
                if (i == 12)
                {
                    UsableMercyJoints[i] = MercyJoints[1].transform;
                }
                if (i == 13)
                {
                    UsableMercyJoints[i] = MercyJoints[2].transform;
                }
                if (i == 14)
                {
                    UsableMercyJoints[i] = MercyJoints[3].transform;
                }
                if (i == 15)
                {
                    UsableMercyJoints[i] = MercyJoints[4].transform;
                }
                if (i == 16)
                {
                    UsableMercyJoints[i] = MercyJoints[0].transform;
                }
                if (i == 17)
                {
                    UsableMercyJoints[i] = MercyJoints[11].transform;
                }
                if (i == 18)
                {
                    UsableMercyJoints[i] = MercyJoints[12].transform;
                }
                if (i == 19)
                {
                    UsableMercyJoints[i] = MercyJoints[13].transform;
                }

            }
            */

            //object2.transform.parent = object1.transform;

            InvokeRepeating("SetObject1Rotation", time, repeatRate);
    }

    // Update is called once per frame
    void Update()
    {
        object01Rotation = object1.transform.rotation;

        var dir = object2.transform.position - object1.transform.position;
        Debug.DrawRay(object1.transform.position, dir, Color.red);
    }

    private void LateUpdate()
    {
        
    }

    public void SetObject1Rotation()
    {
        //We subtract the child object's local position, from the parent object's local position and normalize it to get a direction vector 
        var dir = (object2.transform.localPosition - object1.transform.localPosition).normalized;
        //var rot = Quaternion.LookRotation(dir, new Vector3(0,1,0));//NOT USED
        //rot = new Quaternion(rot.eulerAngles.x, rot.eulerAngles.y, rot.eulerAngles.z, rot.w);
        //object1.transform.rotation = rot;      
        //object1.transform.rotation = Quaternion.RotateTowards(object1.transform.rotation, rot, 1f);

        switch(follow)
        {
            case FollowBehavior.Forward:
                object1.transform.forward = dir;//Sets the forward(blue) vector of the object's rotation to the calcculated direction
                break;
            case FollowBehavior.Up:
                object1.transform.up = dir;//Sets the up(green) vector of the object's rotation to the calcculated direction
                break;
            case FollowBehavior.Right:
                object1.transform.right = dir;//Sets the right(red) vector of the object's rotation to the calcculated direction
                break;
            default:
                break;
        }
        DirData.text = dir.ToString("F3");
        //RotData.text = rot.eulerAngles.ToString("F3");        

        //TestArmRoot.transform.localRotation = rot;
        UsableMercyJoints[2].transform.localRotation = object1.transform.localRotation;
        //UsableMercyJoints[2].transform.LookAt(dir, Vector3.up);
        //UsableMercyJoints[2].transform.rotation = rot;

    }
}
