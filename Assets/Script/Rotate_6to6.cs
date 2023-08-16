using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using static Axis_6to6_loader;


public class Rotate_6to6 : MonoBehaviour
{
    // joint
    public Transform baseJoint;
    public Transform upperbaseJoint;
    public Transform torsoJoint;
    public Transform shoulderJoint;
    public Transform upperarmJoint;
    public Transform armJoint;
    public Transform elbowJoint;
    public Transform forearmJoint;
    public Transform wristJoint;
    public Transform handJoint;

    public Vector3[] axisPositions = new Vector3[6];

    private string dataFilePath;

    Axis_6to6_loader axis_data = new Axis_6to6_loader();

    public int count;

    void Start()
    {
        dataFilePath = Application.dataPath + "/DataSet/Demo/6to6_demo/gt_demo_coor.json";
        count = 0;
        axis_data.txt_reader();
    }

    void Update()
    {       
        if (count < Axis_6to6_loader.coordinate_list.Length)
        {
            upperbaseJoint.localRotation = Quaternion.Euler(0, Axis_6to6_loader.coordinate_list[count, 0], 0);  // 0 a1 0
            torsoJoint.localRotation = Quaternion.Euler(Axis_6to6_loader.coordinate_list[count, 1], 0, 0);  // a2 0 0
            armJoint.localRotation = Quaternion.Euler(Axis_6to6_loader.coordinate_list[count, 2], 0, 0);  // a3 0 0
            forearmJoint.localRotation = Quaternion.Euler(0, Axis_6to6_loader.coordinate_list[count, 3], 0);  // 0 a4 0
            wristJoint.localRotation = Quaternion.Euler(Axis_6to6_loader.coordinate_list[count, 4], 0, 0);  // a5 0 0
            handJoint.localRotation = Quaternion.Euler(0, Axis_6to6_loader.coordinate_list[count, 5], 0);  // 0 a6 0
            // Debug.Log(Axis_6to6_loader.coordinate_list[count, 0] + "," + Axis_6to6_loader.coordinate_list[count, 1] + "," + Axis_6to6_loader.coordinate_list[count, 2] + "," + Axis_6to6_loader.coordinate_list[count, 3] + "," + Axis_6to6_loader.coordinate_list[count, 4] + "," + Axis_6to6_loader.coordinate_list[count, 5]);
            count += 1;
        }

        else if (count == Axis_6to6_loader.coordinate_list.Length)
        {
            upperbaseJoint.localRotation = Quaternion.Euler(0, Axis_6to6_loader.coordinate_list[count, 0], 0);
            torsoJoint.localRotation = Quaternion.Euler(Axis_6to6_loader.coordinate_list[count, 1], 0, 0);
            armJoint.localRotation = Quaternion.Euler(Axis_6to6_loader.coordinate_list[count, 2], 0, 0);
            forearmJoint.localRotation = Quaternion.Euler(0, Axis_6to6_loader.coordinate_list[count, 3], 0);
            wristJoint.localRotation = Quaternion.Euler(Axis_6to6_loader.coordinate_list[count, 4], 0, 0);
            handJoint.localRotation = Quaternion.Euler(0, Axis_6to6_loader.coordinate_list[count, 5], 0);

            count += 0;
        }

       jPosition();
    //    string jointDataJson = JsonUtility.ToJson(new JointData { j1x = axisPositions[0].x, j1y = axisPositions[0].y, j1z = axisPositions[0].z, 
    //                                                            j2x = axisPositions[1].x, j2y = axisPositions[1].y, j2z = axisPositions[1].z, 
    //                                                            j3x = axisPositions[2].x, j3y = axisPositions[2].y, j3z = axisPositions[2].z, 
    //                                                            j4x = axisPositions[3].x, j4y = axisPositions[3].y, j4z = axisPositions[3].z, 
    //                                                            j5x = axisPositions[4].x, j5y = axisPositions[4].y, j5z = axisPositions[4].z,
    //                                                            j6x = axisPositions[5].x, j6y = axisPositions[5].y, j6z = axisPositions[5].z });
    //    File.AppendAllText(dataFilePath, jointDataJson + "\n");
    }

    void jPosition()
    {
        axisPositions[0] = baseJoint.transform.position - baseJoint.transform.position;
        axisPositions[1] = upperarmJoint.transform.position - baseJoint.transform.position;
        axisPositions[2] = elbowJoint.transform.position - baseJoint.transform.position;
        axisPositions[3] = forearmJoint.transform.position - baseJoint.transform.position;
        axisPositions[4] = wristJoint.transform.position - baseJoint.transform.position;
        axisPositions[5] = handJoint.transform.position - baseJoint.transform.position;
        // Debug.Log(axisPositions[0] + "," + axisPositions[1] + "," + axisPositions[2] + "," + axisPositions[3] + "," + axisPositions[4] + "," + axisPositions[5]);
        // Debug.Log(baseJoint.transform.position.ToString("F3") + "," + upperbaseJoint.transform.position.ToString("F3") + "," + torsoJoint.transform.position.ToString("F3") + "," + shoulderJoint.transform.position.ToString("F3") + "," + upperarmJoint.transform.position.ToString("F3") + "," + armJoint.transform.position.ToString("F3") + "," + elbowJoint.transform.position.ToString("F3") + "," + forearmJoint.transform.position.ToString("F3") + "," + wristJoint.transform.position.ToString("F3") + "," + handJoint.transform.position.ToString("F3"));
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
    }
}
