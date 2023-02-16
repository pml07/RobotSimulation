using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System;
using System.Threading.Tasks;
using System.Threading;
using System.Collections;
using System.Linq;


public class RobotControl : MonoBehaviour
{
    // receive
    Socket server;
    public int receivePort = 5060;
    string receiveHost = "127.0.0.1";
    Thread t;

    // send
    Socket client;
    public int sendPort = 5061;
    string sendHost = "127.0.0.1";

    // joint
    public Transform torsoJoint;
    public Transform leftShoulderForwardJoint;
    public Transform leftShoulderUpJoint;
    public Transform leftElbowJoint;
    public Transform leftWristJoint;
    public Transform leftHandJoint;
    
    public float[] jointRotations = new float[6];
    public Vector3[] jointPositions = new Vector3[6];


    void Start()
    {
        server = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
        server.Bind(new IPEndPoint(IPAddress.Parse(receiveHost), receivePort));
        Debug.Log("------- Listening on port " + receivePort + " -------");

        client = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
        Debug.Log("------- Sending data to " + sendHost + " on port " + sendPort + " -------");

        t = new Thread(new ThreadStart(ReceiveMsg));
        t.Start();
    }

    void Update()
    {
        torsoJoint.localRotation = Quaternion.Euler(0, jointRotations[0], 0);  // 0 a1 0
        leftShoulderForwardJoint.localRotation = Quaternion.Euler(jointRotations[1], 0, 0);  // a2 0 0
        leftShoulderUpJoint.localRotation = Quaternion.Euler(jointRotations[2], 0, 0);  // a3 0 0
        leftElbowJoint.localRotation = Quaternion.Euler(0, jointRotations[3], 0);  // 0 a4 0
        leftWristJoint.localRotation = Quaternion.Euler(jointRotations[4], 0, 0);  // a5 0 0
        leftHandJoint.localRotation = Quaternion.Euler(0, jointRotations[5], 0);  // 0 a6 0

        jPosition();
    }

    void ReceiveMsg()
    {
        EndPoint receiveEndPoint = new IPEndPoint(IPAddress.Parse(receiveHost), receivePort);
        while (true)
        {
            EndPoint point;
            point = new IPEndPoint(IPAddress.Any, 0);
            
            byte[] buffer = new byte[1024];
            int length = server.ReceiveFrom(buffer, ref point);

            string message = Encoding.UTF8.GetString(buffer, 0, length);
            // Debug.Log(message);
            // Debug.Log(point.ToString());

            if (message.Contains(","))
            {
                string[] a1a6 = message.Split(new string[] { "," }, StringSplitOptions.RemoveEmptyEntries);

                jointRotations[0] = float.Parse(a1a6[0]);
                jointRotations[1] = float.Parse(a1a6[1]);
                jointRotations[2] = float.Parse(a1a6[2]);
                jointRotations[3] = float.Parse(a1a6[3]);
                jointRotations[4] = float.Parse(a1a6[4]);
                jointRotations[5] = float.Parse(a1a6[5]);
            }
            else
            {
                Debug.Log("-------- No data received. --------");
            }
        }
    }
    
    void SendMsg()
    {
        string message = string.Join(";", jointPositions.Select(p => p.ToString()).ToArray());
        Debug.Log(message);
        byte[] buffer = Encoding.UTF8.GetBytes(message);
        client.SendTo(buffer, new IPEndPoint(IPAddress.Parse(sendHost), sendPort));
    }

    void jPosition()
    {
        jointPositions[0] = torsoJoint.transform.position;
        jointPositions[1] = leftShoulderForwardJoint.transform.position;
        jointPositions[2] = leftShoulderUpJoint.transform.position;
        jointPositions[3] = leftElbowJoint.transform.position;
        jointPositions[4] = leftWristJoint.transform.position;
        jointPositions[5] = leftHandJoint.transform.position;

        SendMsg();
    }
}
