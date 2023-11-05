using System;
using System.Threading;
using UnityEngine;
using UnityEngine.UI;
using Intel.RealSense;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEditor.AnimatedValues;
using UnityEditor.Animations;
using System.IO;
using Vuforia;
using Intel.RealSense.Math;

namespace Cubemos
{
    public class MAD_Tracker_Max : MonoBehaviour
    {
        //List variable to hold the skeletons detected by the Real Sense Sensor
        [SerializeField]
        public List<Skeleton> lastSkeletons;

        //Dictionary variable of detected skeletal joints from the Real Sense Sensor
        [SerializeField]
        public Dictionary<int, Skeleton.Joint> rsJoints;

        //Variable to hold our User Avatar Game Object
        [SerializeField]
        public GameObject MAD_Avatar;

        //Variable to hold our Target Avatar Game Object
        [SerializeField]
        public GameObject MAD_Target;

        //Variable to hold the world's root origin
        [SerializeField]
        public GameObject PrevizRoot;

        //This holds the Game Objects to be used to instantiate as a previz sphere for our detected skeletal points
        public GameObject skeletalJoint;

        //Array of gameobjects for previz game objects
        [SerializeField]
        public GameObject[] SkeletalList;

        //Array of Transform objects, specifically joints, of our user avatar
        [SerializeField]
        private Transform[] avatarJoints;

        //A transform array of only the trackable joints needed
        [SerializeField]
        public Transform[] trackableAvatarJoints;

        [SerializeField]
        public GameObject[] approximationParts;

        //Variable to control frequency of data update
        [SerializeField]
        public float freq = 0.5f;

        [SerializeField]
        public float hipOffset = 0.1f;

        [SerializeField]
        public float spineOffset = -0.1f;

        [SerializeField]
        public float spine1Offset = -0.2f;

        [SerializeField]
        public float spine2Offset = -0.2f;

        //Variable to hold our animator controller to trigger user mocap animations to follow
        [SerializeField]
        public Animator MAD_Animator;

        //Variable reference to a UI button to start the animation
        [SerializeField]
        public Button MAD_Squat_Start;

        //Variable reference to a UI button to stop the animation
        [SerializeField]
        public Button MAD_Squat_Stop;

        //Variable reference to a UI button to start the animation
        [SerializeField]
        public Button MAD_LungesTest_Start;

        //Variable reference to a UI button to stop the animation
        [SerializeField]
        public Button MAD_LungesTest_Stop;

        [SerializeField]
        public Button MAD_ArmRaise_Start;

        //Variable reference to a UI button to stop the animation
        [SerializeField]
        public Button MAD_ArmRaise_Stop;

        //Variable reference to a UI button to stop the animation
        [SerializeField]
        public Button MAD_HideTargetAvatar;

        //Variable reference to a UI button to stop the animation
        [SerializeField]
        public Button MAD_ShowTargetAvatar;

        //variable to hold the transform parent of our user avatar skeleton
        public Transform targetHipBone;

        //variable to hold the transform parent of our user avatar skeleton
        public Transform userHipBone;

        //Variables to access Cubemos Systems and Real Sense Sensor data
        private SkeletonTracker mySkelTracker;
        private RealsenseManager myRealSenseManager;

        //variable indicating the size of tracked point for the Intel Real Sense Sensor
        private int SkeletonSize = 18;

        //Private boolean to find status of current animation playback
        bool MAD_Squat;

        //Private boolean to find status of current animation playback
        bool MAD_ArmRaise;

        //Private boolean to find status of current animation playback
        bool MAD_LungesTest;

        //Private boolean to find status of current animation playback
        bool MAD_TargetAvatarVis;

        // Start is called before the first frame update
        void Start()
        {
            
            MAD_Squat = false;
            MAD_ArmRaise = false;
            MAD_LungesTest = false;
            MAD_TargetAvatarVis = false;
            //Start the RealSense Sensor and the Cubemos skeleton tracker
            mySkelTracker = new SkeletonTracker();
            myRealSenseManager = new RealsenseManager();

            //Initializes the cubemos system and the real sense sensor
            mySkelTracker.Initialize();
            myRealSenseManager.Initialize();

            //Creates instances of our User avatar as well as our previz root location
            MAD_Avatar = Instantiate(MAD_Avatar, new Vector3(0, 0, 0), UnityEngine.Quaternion.identity);
            MAD_Target = Instantiate(MAD_Target, new Vector3(0, 0, 0), UnityEngine.Quaternion.identity);
            PrevizRoot = Instantiate(PrevizRoot, new Vector3(0, 0, 0), UnityEngine.Quaternion.identity);

            MAD_Target.SetActive(false);
            //MAD_Avatar.SetActive(false);
            //Finds the Target Hip Bone transform, sets it to avariable and centers it on the screen
            targetHipBone = MAD_Target.transform.GetChild(2);
            targetHipBone.transform.position = new Vector3(0, 0, 0);
            targetHipBone.transform.rotation = new UnityEngine.Quaternion(0, 0, 0, 0);

            //Finds the User Hip Bone transform, sets it to avariable and centers it on the screen
            userHipBone = MAD_Avatar.transform.GetChild(2);
            userHipBone.transform.position = new Vector3(0, 0, 0);
            userHipBone.transform.rotation = new UnityEngine.Quaternion(0, 0, 0, 0);

            //Sets the position of our avatar and target prefab
            MAD_Target.transform.position = new Vector3(0, -1.04f, -0.2f);
            MAD_Avatar.transform.position = new Vector3(0, 0, 0);

            //Loads the Animator component of our Avatar prefab into a variable
            MAD_Animator = MAD_Target.GetComponent<Animator>();

            //Loads the main 18 trackable points to an accessible array. 
            //Due to our rigs not having a use for ear tracking, we are only making an array of 16 trackable points.
            //The last two points of data are being discarded. These include left and right ear tracked points.
            avatarJoints = userHipBone.GetComponentsInChildren<Transform>();
            trackableAvatarJoints = new Transform[SkeletonSize - 2];//makes the new array from our variable at the defined size
            for (int i = 0; i<SkeletonSize-2; i++)
            {
                //head
                if (i == 0)
                {
                    trackableAvatarJoints[i] = avatarJoints[39];
                }
                //neck
                if (i == 1)
                {
                    trackableAvatarJoints[i] = avatarJoints[38];
                }
                //right shoulder
                if (i == 2)
                {
                    trackableAvatarJoints[i] = avatarJoints[44];
                }
                //right elbow
                if (i == 3)
                {
                    trackableAvatarJoints[i] = avatarJoints[45];
                }
                //right hand
                if (i == 4)
                {
                    trackableAvatarJoints[i] = avatarJoints[46];
                }
                //left shoulder
                if (i == 5)
                {
                    trackableAvatarJoints[i] = avatarJoints[15];
                }
                //left elbow
                if (i == 6)
                {
                    trackableAvatarJoints[i] = avatarJoints[16];
                }
                //left hand
                if (i == 7)
                {
                    trackableAvatarJoints[i] = avatarJoints[17];
                }
                //right Thigh
                if (i == 8)
                {
                    trackableAvatarJoints[i] = avatarJoints[6];
                }
                //right Knee
                if (i == 9)
                {
                    trackableAvatarJoints[i] = avatarJoints[7];
                }
                //right Ankle
                if (i == 10)
                {
                    trackableAvatarJoints[i] = avatarJoints[8];
                }
                //left Thigh
                if (i == 11)
                {
                    trackableAvatarJoints[i] = avatarJoints[1];
                }
                //left Knee
                if (i == 12)
                {
                    trackableAvatarJoints[i] = avatarJoints[2];
                }
                //left Ankle
                if (i == 13)
                {
                    trackableAvatarJoints[i] = avatarJoints[3];
                }
                //right eye
                if (i == 14)
                {
                    trackableAvatarJoints[i] = avatarJoints[42];
                }
                //left eye
                if (i == 15)
                {
                    trackableAvatarJoints[i] = avatarJoints[41];
                }
                
            }

            //Creates a new array of SkeletalList and populates it with spheres for visual representation
            //Using spheres as they hold a full transform of position and rotation as well as scale
            SkeletalList = new GameObject[SkeletonSize];
            for (int i = 0; i < SkeletonSize; i++)
            {
                //Creates by instances proxy meshes and names each of them according to their placement
                GameObject aJoint = Instantiate(skeletalJoint, new Vector3(0, (float)i - 0.8f, 0), UnityEngine.Quaternion.identity) as GameObject;
                if (i == 0)
                {
                    aJoint.name = "MAD_noseJoint";
                }
                if (i == 1)
                {
                    aJoint.name = "MAD_neckJoint";
                }
                if (i == 2)
                {
                    aJoint.name = "MAD_rightShoulderJoint";
                }
                if (i == 3)
                {
                    aJoint.name = "MAD_rightElbowJoint";
                }
                if (i == 4)
                {
                    aJoint.name = "MAD_rightWristJoint";
                }
                if (i == 5)
                {
                    aJoint.name = "MAD_leftShoulderJoint";
                }
                if (i == 6)
                {
                    aJoint.name = "MAD_leftElbowJoint";
                }
                if (i == 7)
                {
                    aJoint.name = "MAD_leftWristJoint";
                }
                if (i == 8)
                {
                    aJoint.name = "MAD_rightThighJoint";
                }
                if (i == 9)
                {
                    aJoint.name = "MAD_rightKneeJoint";
                }
                if (i == 10)
                {
                    aJoint.name = "MAD_rightAnkleJoint";
                }
                if (i == 11)
                {
                    aJoint.name = "MAD_leftThighJoint";
                }
                if (i == 12)
                {
                    aJoint.name = "MAD_leftKneeJoint";
                }
                if (i == 13)
                {
                    aJoint.name = "MAD_leftAnkleJoint";
                }
                if (i == 14)
                {
                    aJoint.name = "MAD_rightEyeJoint";
                }
                if (i == 15)
                {
                    aJoint.name = "MAD_leftEyeJoint";
                }
                if (i == 16)
                {
                    aJoint.name = "MAD_rightEarJoint";
                }
                if (i == 17)
                {
                    aJoint.name = "MAD_leftEarJoint";
                }

                SkeletalList[i] = aJoint;
            }

            approximationParts = new GameObject[4];
            for (int i = 0; i < 4; i++)
            {
                GameObject aproxJoint = Instantiate(skeletalJoint, new Vector3(0, 0, 0), UnityEngine.Quaternion.identity) as GameObject;

                if (i == 0)
                {
                    aproxJoint.name = "MAD_hips";
                }
                if (i == 1)
                {
                    aproxJoint.name = "MAD_spine";
                }
                if (i == 2)
                {
                    aproxJoint.name = "MAD_spine1";
                }
                if (i == 3)
                {
                    aproxJoint.name = "MAD_spine2";
                }

                approximationParts[i] = aproxJoint;
            }
            
            //Checks the frames from the sensor and updates our proxy skeletal objects every 1/10th of a second.
            InvokeRepeating("MAD_SetJointPositions", 0.1f, 0.1f);

        }
        //Method to iterate through sensor detected skeletons and setting the positions of our proxy meshes to their locations
        void MAD_SetJointPositions()
        {
            //Gets the current frame being captured by the Real Sense Sensor           
            using (var frame = myRealSenseManager.GetFrame())
            {
                //Extrapolates the skeletal points from the image feed supplied by the RealSense Sensor.
                //It uses the ColorFrames and the DepthFrames to determine the position of joints on detected skeletons.
                lastSkeletons = mySkelTracker.TrackSkeletonsWithRealsenseFrames(frame.ColorFrame, frame.DepthFrame, myRealSenseManager.Intrinsics);
                
                foreach (var sk in lastSkeletons)//for each skeleton in the skeletons detected
                {
                    if (sk.Index <= 0)//if it is the first skeleton found
                    {
                        foreach (var j in sk.Joints)//for each joint found in skeleton
                        {                            
                            //Sets each instance of our proxy joint meshes to a detected skeletal point on the sensor data
                            SkeletalList[j.Key].transform.position = Vector3.MoveTowards(SkeletalList[j.Key].transform.position, (j.Value.position*-1), freq);                        
                        }
                    }
                }
            }
            approximationParts[3].transform.position = Vector3.MoveTowards(approximationParts[3].transform.position, (SkeletalList[2].transform.position + SkeletalList[5].transform.position) * 0.5f, freq);
            approximationParts[0].transform.position = Vector3.MoveTowards(approximationParts[0].transform.position, new Vector3(SkeletalList[1].transform.position.x, SkeletalList[1].transform.position.y-0.5f, SkeletalList[1].transform.position.z ), freq);
            approximationParts[1].transform.position = Vector3.MoveTowards(approximationParts[1].transform.position, (approximationParts[0].transform.position + approximationParts[3].transform.position) * 0.25f, freq);
            approximationParts[2].transform.position = Vector3.MoveTowards(approximationParts[2].transform.position, (approximationParts[0].transform.position + approximationParts[3].transform.position) * 0.75f, freq);      
        }
        
        // Update is called once per frame
        void Update()
        {
            //MAD_SetJointPositions();
            //Draws Debug Rays from the Nose Joint to the Eye Joints and from the Nose Joint to the Neck Joint
            Debug.DrawRay(SkeletalList[0].transform.position, SkeletalList[14].transform.position - SkeletalList[0].transform.position, Color.green);
            Debug.DrawRay(SkeletalList[0].transform.position, SkeletalList[15].transform.position - SkeletalList[0].transform.position, Color.green);
            Debug.DrawRay(SkeletalList[1].transform.position, SkeletalList[0].transform.position - SkeletalList[1].transform.position, Color.green);
            
            //Draws Debug Rays from the Neck Joint to the right arm and its children
            Debug.DrawRay(SkeletalList[1].transform.position, SkeletalList[2].transform.position - SkeletalList[1].transform.position, Color.red);
            Debug.DrawRay(SkeletalList[2].transform.position, SkeletalList[3].transform.position - SkeletalList[2].transform.position, Color.red);
            Debug.DrawRay(SkeletalList[3].transform.position, SkeletalList[4].transform.position - SkeletalList[3].transform.position, Color.red);

            //Draws Debugt Rays from the Neck Joint to the left arm and its children
            Debug.DrawRay(SkeletalList[1].transform.position, SkeletalList[5].transform.position - SkeletalList[1].transform.position, Color.blue);            
            Debug.DrawRay(SkeletalList[5].transform.position, SkeletalList[6].transform.position - SkeletalList[5].transform.position, Color.blue);
            Debug.DrawRay(SkeletalList[6].transform.position, SkeletalList[7].transform.position - SkeletalList[6].transform.position, Color.blue);

            //Draws Debug Rays from the Neck Joint to the right leg and its children
            Debug.DrawRay(SkeletalList[1].transform.position, SkeletalList[8].transform.position - SkeletalList[1].transform.position, Color.red);
            Debug.DrawRay(SkeletalList[8].transform.position, SkeletalList[9].transform.position - SkeletalList[8].transform.position, Color.red);
            Debug.DrawRay(SkeletalList[9].transform.position, SkeletalList[10].transform.position - SkeletalList[9].transform.position, Color.red);
            
            //Draws Debug Rays from Neck Joint to the left leg and its children
            Debug.DrawRay(SkeletalList[1].transform.position, SkeletalList[11].transform.position - SkeletalList[1].transform.position, Color.blue);
            Debug.DrawRay(SkeletalList[11].transform.position, SkeletalList[12].transform.position - SkeletalList[11].transform.position, Color.blue);
            Debug.DrawRay(SkeletalList[12].transform.position, SkeletalList[13].transform.position - SkeletalList[12].transform.position, Color.blue);
            
            //Draws Debug Rays from Eye Joints to Ear Joints
            Debug.DrawRay(SkeletalList[14].transform.position, SkeletalList[16].transform.position - SkeletalList[14].transform.position, Color.red);
            Debug.DrawRay(SkeletalList[15].transform.position, SkeletalList[17].transform.position - SkeletalList[15].transform.position, Color.blue);

            if (MAD_Squat == false && MAD_ArmRaise != true)
            {
                MAD_Squat_Start.onClick.AddListener(doSquat);
                MAD_Squat = true;
            }
            if (MAD_Squat == true || MAD_ArmRaise == true || MAD_LungesTest == true)
            {
                MAD_Squat_Stop.onClick.AddListener(goTPose);
                MAD_ArmRaise_Stop.onClick.AddListener(goTPose);
                MAD_LungesTest_Start.onClick.AddListener(goTPose);
                MAD_Squat = false;
                MAD_ArmRaise = false;
                MAD_LungesTest = false;
            }
            if (MAD_ArmRaise == false && MAD_Squat != true)
            {
                MAD_ArmRaise_Start.onClick.AddListener(doArmRaise);
                MAD_ArmRaise = true;
            }  
            if(MAD_LungesTest == false)
            {
                MAD_LungesTest_Start.onClick.AddListener(doLunges);
                MAD_LungesTest = true;
            }
            if(MAD_TargetAvatarVis == true)
            {
                MAD_HideTargetAvatar.onClick.AddListener(hideTarget);
                
            }
            if(MAD_TargetAvatarVis == false)
            {
                MAD_ShowTargetAvatar.onClick.AddListener(showTarget);
                             
            }
        }
        private void LateUpdate()
        {            
            //This line sets the hip position in wordl space to the neck joint position of the tracker data with a hipoffset on the Y axis.
            //avatarJoints[0].transform.position = Vector3.MoveTowards(avatarJoints[0].transform.position, new Vector3(SkeletalList[1].transform.position.x, 0, SkeletalList[1].transform.position.z), freq);

            //Rotation approximation for the right shoulder
            var dir = calculateDirection(SkeletalList[2], SkeletalList[3]);
            SkeletalList[2].transform.right = dir;
            trackableAvatarJoints[2].transform.localRotation = SkeletalList[2].transform.localRotation;

            //Rotation approximation for the right elbow
            dir = calculateDirection(SkeletalList[3], SkeletalList[4]);
            SkeletalList[3].transform.right = dir;
            trackableAvatarJoints[3].transform.localRotation = SkeletalList[3].transform.localRotation;

            //Rotation approximation for the left shoulder
            dir = calculateDirection(SkeletalList[5], SkeletalList[6]);
            SkeletalList[5].transform.right = dir*-1;
            trackableAvatarJoints[5].transform.localRotation = SkeletalList[5].transform.localRotation;

            //Rotation approximation for the left elbow
            dir = calculateDirection(SkeletalList[6], SkeletalList[7]);
            SkeletalList[6].transform.right = dir*-1;
            trackableAvatarJoints[6].transform.localRotation = SkeletalList[6].transform.localRotation;

            //Rotation approximation for the right thigh
            dir = calculateDirection(SkeletalList[8], SkeletalList[9]);
            SkeletalList[8].transform.up = dir * -1;
            trackableAvatarJoints[8].transform.localRotation = SkeletalList[8].transform.localRotation;

            //Rotation approximation for the right knee
            dir = calculateDirection(SkeletalList[9], SkeletalList[10]);
            SkeletalList[9].transform.up = dir * -1;
            trackableAvatarJoints[9].transform.localRotation = SkeletalList[9].transform.localRotation;

            //Rotation approximation for the left thigh
            dir = calculateDirection(SkeletalList[11], SkeletalList[12]);
            SkeletalList[11].transform.up = dir * -1;
            trackableAvatarJoints[11].transform.localRotation = SkeletalList[11].transform.localRotation;

            //Rotation approximation for the left knee
            dir = calculateDirection(SkeletalList[12], SkeletalList[13]);
            SkeletalList[12].transform.up = dir * -1;
            trackableAvatarJoints[12].transform.localRotation = SkeletalList[12].transform.localRotation;

            //Rotation approximation for the neck
            dir = calculateDirection(SkeletalList[1], SkeletalList[0]);
            SkeletalList[1].transform.up = dir;
            trackableAvatarJoints[1].transform.localRotation = SkeletalList[1].transform.localRotation;

        }

        Vector3 calculateDirection(GameObject object1, GameObject object2)
        {
            //Determines the direction of a vector based on the child object's position being subtracted from the parent object's position
            var dir = (object2.transform.localPosition - object1.transform.localPosition).normalized;
            //Returns the calculated Vector value for us to use
            return dir;
        }
        void showTarget()
        {
            MAD_Target.SetActive(true);
            MAD_TargetAvatarVis = true;
            //Debug.Log("Pressed Show Target");
        }
        void hideTarget()
        {
            MAD_Target.SetActive(false);
            MAD_TargetAvatarVis = false;
            //Debug.Log("Pressed Hide Target");
        }
        void doSquat()
        {
            //Enables squat animation, disables the squat start button, and enables the squat stop button
            MAD_Animator.SetBool("Squat", true);
            MAD_Squat_Start.enabled = false;
            MAD_Squat_Stop.enabled = true;
            //Debug.Log("Pressed Start Squat"); 
        }
        void goTPose()
        {
            //Stops squat animation, disables the squat stop button, and enables the squat start button
            MAD_Animator.SetBool("Squat", false);
            MAD_Animator.SetBool("ArmRaise", false);
            MAD_Animator.SetBool("LungesTest", false);
            MAD_Squat_Start.enabled = true;
            MAD_Squat_Stop.enabled = false;
            MAD_ArmRaise_Start.enabled = true;
            MAD_ArmRaise_Stop.enabled = false;
            MAD_LungesTest_Start.enabled = true;
            MAD_LungesTest_Stop.enabled = false;
            //Debug.Log("Pressed Stop");
        }
        void doArmRaise()
        {
            MAD_Animator.SetBool("ArmRaise", true);          
            MAD_ArmRaise_Start.enabled = false;
            MAD_ArmRaise_Stop.enabled = true;
            //Debug.Log("Pressed Arm Raises");
        }
        void doLunges()
        {
            MAD_Animator.SetBool("LungesTest", true);
            MAD_LungesTest_Start.enabled = false;
            MAD_LungesTest_Stop.enabled = true;
            //Debug.Log("Pressed Lunges");
        }
        void Mad_SaveRecordData()
        {

        }
        void Mad_WriteDataToFile()
        {

        }

    }
    
    public struct Dictionary<MAD_JointData>
    {
        string JointName;
        string JointIndex;
        Vector3 JointPosition;
        AnimQuaternion JointQuaternion;
        int DataRecordTime;
        
    }
   
}