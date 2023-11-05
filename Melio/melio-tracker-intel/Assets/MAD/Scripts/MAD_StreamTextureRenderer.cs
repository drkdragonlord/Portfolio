using Intel.RealSense;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Threading;
using UnityEngine;
using UnityEngine.Events;

namespace Cubemos
{
    public class MAD_StreamTextureRenderer : MonoBehaviour
    {
        public int frameWidth;
        public int frameHeight;

        private RealsenseManager myRealSenseManager;

        protected Texture2D texture;

        public
        // Start is called before the first frame update
        void Start()
        {
            myRealSenseManager = new RealsenseManager();

            myRealSenseManager.Initialize();

        }

        // Update is called once per frame
        void Update()
        {
            using (var frame = myRealSenseManager.GetFrame().ColorFrame)
                texture = new Texture2D(frameWidth, frameHeight);
        }
    }
}
