using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;


public class Rotate : MonoBehaviour
{
    // joint
    public Transform baseJoint;//
    public Transform upperbaseJoint;
    public Transform torsoJoint; //
    public Transform shoulderJoint;
    public Transform upperarmJoint; //
    public Transform armJoint;
    public Transform elbowJoint; //
    public Transform forearmJoint;
    public Transform wristJoint;
    public Transform handJoint;
    public Transform endJoint; //

    public float[] jointRotations = new float[6];
    public Vector3[] axisPositions = new Vector3[6];

    private string dataFilePath;


    void Start()
    {
        dataFilePath = Application.dataPath + "/Script/joint_1.json";
    }

    void Update()
    {
        float prev0Rotation = jointRotations[0];
        float new0Rotation = Mathf.Clamp(Random.Range(prev0Rotation - 3f, prev0Rotation + 3f), -165f, 165f);  // -165~165
        jointRotations[0] = new0Rotation;
        prev0Rotation = new0Rotation;
    
        float prev1Rotation = jointRotations[1];
        float new1Rotation = Mathf.Clamp(Random.Range(prev1Rotation - 3f, prev1Rotation + 3f), -125f, 85f);  // -125~85
        jointRotations[1] = new1Rotation;
        prev1Rotation = new1Rotation;

        float prev2Rotation = jointRotations[2];
        float new2Rotation = Mathf.Clamp(Random.Range(prev2Rotation - 3f, prev2Rotation + 3f), -55f, 185f);  // -55~185
        jointRotations[2] = new2Rotation;
        prev2Rotation = new2Rotation;

        float prev3Rotation = jointRotations[3];
        float new3Rotation = Mathf.Clamp(Random.Range(prev3Rotation - 3f, prev3Rotation + 3f), -190f, 190f);  // -190~190
        jointRotations[3] = new3Rotation;
        prev3Rotation = new3Rotation;

        float prev4Rotation = jointRotations[4];
        float new4Rotation = Mathf.Clamp(Random.Range(prev4Rotation - 3f, prev4Rotation + 3f), -115f, 115f);  // -115~115
        jointRotations[4] = new4Rotation;
        prev4Rotation = new4Rotation;

        float prev5Rotation = jointRotations[5];
        float new5Rotation = Mathf.Clamp(Random.Range(prev5Rotation - 1f, prev5Rotation + 1f), -2f, 2f);  // -360~360
        jointRotations[5] = new5Rotation;
        prev5Rotation = new5Rotation;

        upperbaseJoint.localRotation = Quaternion.Euler(0, jointRotations[0], 0);  // 0 a1 0
        torsoJoint.localRotation = Quaternion.Euler(jointRotations[1], 0, 0);  // a2 0 0
        armJoint.localRotation = Quaternion.Euler(jointRotations[2], 0, 0);  // a3 0 0
        forearmJoint.localRotation = Quaternion.Euler(0, jointRotations[3], 0);  // 0 a4 0
        wristJoint.localRotation = Quaternion.Euler(jointRotations[4], 0, 0);  // a5 0 0
        handJoint.localRotation = Quaternion.Euler(0, jointRotations[5], 0);  // 0 a6 0

        jPosition();

        string jointDataJson = JsonUtility.ToJson(new JointData { j1x = axisPositions[0].x, j1y = axisPositions[0].y, j1z = axisPositions[0].z, j2x = axisPositions[1].x, j2y = axisPositions[1].y, j2z = axisPositions[1].z, j3x = axisPositions[2].x, j3y = axisPositions[2].y, j3z = axisPositions[2].z, j4x = axisPositions[3].x, j4y = axisPositions[3].y, j4z = axisPositions[3].z, j5x = axisPositions[4].x, j5y = axisPositions[4].y, j5z = axisPositions[4].z, j6x = axisPositions[5].x, j6y = axisPositions[5].y, j6z = axisPositions[5].z, rot1 = jointRotations[0], rot2 = jointRotations[1], rot3 = jointRotations[2], rot4 = jointRotations[3], rot5 = jointRotations[4], rot6 = jointRotations[5] });
        File.AppendAllText(dataFilePath, jointDataJson + "\n");
    }

    void jPosition()
    {        
        axisPositions[0] = baseJoint.transform.position - baseJoint.transform.position;  // axis 1 端點: base_link
        axisPositions[1] = shoulderJoint.transform.position - baseJoint.transform.position;  // axis 2 端點: shoulder_link
        axisPositions[2] = armJoint.transform.position - baseJoint.transform.position;  // axis 3 端點: arm_link
        axisPositions[3] = forearmJoint.transform.position - baseJoint.transform.position;  // axis 4 端點: forearm_link
        axisPositions[4] = handJoint.transform.position - baseJoint.transform.position;  // axis 5 端點: hand_link
        axisPositions[5] = wristJoint.transform.position - baseJoint.transform.position;  // axis 6 端點: wrist_link
        Debug.Log(axisPositions[0] + "," + axisPositions[1] + "," + axisPositions[2] + "," + axisPositions[3] + "," + axisPositions[4] + "," + axisPositions[5]);
    }

    [System.Serializable]
    private class JointData
    {
        public float j1x;
        public float j1y;
        public float j1z;
        public float j2x;
        public float j2y;
        public float j2z;
        public float j3x;
        public float j3y;
        public float j3z;
        public float j4x;
        public float j4y;
        public float j4z;
        public float j5x;
        public float j5y;
        public float j5z;
        public float j6x;
        public float j6y;
        public float j6z;
        public float rot1;
        public float rot2;
        public float rot3;
        public float rot4;
        public float rot5;
        public float rot6;
    }
}
