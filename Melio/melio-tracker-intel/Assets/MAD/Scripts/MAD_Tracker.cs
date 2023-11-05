using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Cubemos
{
    public class MAD_Tracker : MonoBehaviour
    {
        [SerializeField]
        public List<Skeleton> lastSkeletons;

        [SerializeField]
        public Dictionary<int, Skeleton.Joint> rsJoints;

        public GameObject skeletalJoint;

        private SkeletonTracker mySkelTracker;
        private RealsenseManager myRealSenseManager;

        private int SkeletonSize = 18;
        [SerializeField]
        public GameObject[] SkeletalList;        

        // Start is called before the first frame update
        void Start()
        {
            //Start the RealSense Sensor and the Cubemos skeleton tracker
            mySkelTracker = new SkeletonTracker();
            myRealSenseManager = new RealsenseManager();

            mySkelTracker.Initialize();
            myRealSenseManager.Initialize();

            //Creates a new array of SkeletalList and populates it with spheres for visual representation
            //Using spheres as they hold a full transform of position and rotation as well as scale
            SkeletalList = new GameObject[SkeletonSize];
            for (int i = 0; i < SkeletonSize; i++)
            {
                GameObject aJoint = Instantiate(skeletalJoint, new Vector3(0, (float)i-0.8f, 0), Quaternion.identity) as GameObject;
                SkeletalList[i] = aJoint;
            }            

        }//Closes void Start

        // Update is called once per frame
        void Update()
        {
            //Gets the feed from the RealSense Sensor
            using (var frame = myRealSenseManager.GetFrame())
            {
                //Extrapolates the skletal points from the image feed supplied by the RealSense Sensor.
                //It uses the ColorFrames and the DepthFrames to determine the position of joints on detected skeletons.
                lastSkeletons = mySkelTracker.TrackSkeletonsWithRealsenseFrames(frame.ColorFrame, frame.DepthFrame, myRealSenseManager.Intrinsics);

                foreach (var sk in lastSkeletons)
                {    
                    foreach (var j in sk.Joints)
                    {
                        float freq = 0.3f;
                        Debug.Log("This is Joints number " + j.Key);
                        SkeletalList[j.Key].transform.position = Vector3.MoveTowards(SkeletalList[j.Key].transform.position, j.Value.position, freq);
                        /*
                        for (int i = 0; i < sk.Joints.Count; i++)
                        {
                            SkeletalList[i].transform.position = Vector3.MoveTowards(SkeletalList[i].transform.position, j.Value.position, freq);
                        }                            
                        if (sk.Index == 0)
                        {
                            SkeletalList[0].transform.position = Vector3.MoveTowards(SkeletalList[0].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 1)
                        {
                            SkeletalList[1].transform.position = Vector3.MoveTowards(SkeletalList[1].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 2)
                        {
                            SkeletalList[2].transform.position = Vector3.MoveTowards(SkeletalList[2].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 3)
                        {
                            SkeletalList[3].transform.position = Vector3.MoveTowards(SkeletalList[3].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 4)
                        {
                            SkeletalList[4].transform.position = Vector3.MoveTowards(SkeletalList[4].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 5)
                        {
                            SkeletalList[5].transform.position = Vector3.MoveTowards(SkeletalList[5].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 6)
                        {
                            SkeletalList[6].transform.position = Vector3.MoveTowards(SkeletalList[6].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 7)
                        {
                            SkeletalList[7].transform.position = Vector3.MoveTowards(SkeletalList[7].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 8)
                        {
                            SkeletalList[8].transform.position = Vector3.MoveTowards(SkeletalList[8].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 9)
                        {
                            SkeletalList[9].transform.position = Vector3.MoveTowards(SkeletalList[9].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 10)
                        {
                            SkeletalList[10].transform.position = Vector3.MoveTowards(SkeletalList[10].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 11)
                        {
                            SkeletalList[11].transform.position = Vector3.MoveTowards(SkeletalList[11].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 12)
                        {
                            SkeletalList[12].transform.position = Vector3.MoveTowards(SkeletalList[12].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 13)
                        {
                            SkeletalList[13].transform.position = Vector3.MoveTowards(SkeletalList[13].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 14)
                        {
                            SkeletalList[14].transform.position = Vector3.MoveTowards(SkeletalList[14].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 15)
                        {
                            SkeletalList[15].transform.position = Vector3.MoveTowards(SkeletalList[15].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 16)
                        {
                            SkeletalList[16].transform.position = Vector3.MoveTowards(SkeletalList[16].transform.position, j.Value.position, freq);
                        }
                        if (sk.Index == 17)
                        {
                            SkeletalList[17].transform.position = Vector3.MoveTowards(SkeletalList[17].transform.position, j.Value.position, freq);
                        }*/
                    }//Closes foreach (var j in sk.Joints) 
                    

                }//Closes foreach (var sk in lastSkeletons)
            }//Closes using (var frame = myRealSenseManager.GetFrame())
        }//Closes void Update
    }//Closes MAD_Tracker
}//Closes namespace Cubemos
