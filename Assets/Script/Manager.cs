using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System;
using System.Threading.Tasks;
using System.Threading;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Collections.Concurrent;


public class TrainingManager : MonoBehaviour
{
    string host = "127.0.0.1";
    Socket client;
    public int port = 8080;
    Thread t;

    const int messageLength = 10000; //12000
    byte[] messageHolder = new byte[messageLength];
    readonly ConcurrentQueue<string> inMessage = new ConcurrentQueue<string>();

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

    private bool couldSend = false;

    void Start()
    {
        client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        client.Connect(IPAddress.Parse(host), port);
        Debug.Log("Start listening...");
    }


    void Update()
    {
        ThreadReceive();
        while (inMessage.TryDequeue(out string jm))
        {
            try
            {
                Receive(jm);
            }
            catch (Exception e)
            {
                Debug.LogException(e, this);
                Debug.Log(jm);
            }
        }
        upperbaseJoint.localRotation = Quaternion.Euler(0, jointRotations[0], 0);  // 0 a1 0
        shoulderJoint.localRotation = Quaternion.Euler(jointRotations[1], 0, 0);  // a2 0 0
        armJoint.localRotation = Quaternion.Euler(jointRotations[2], 0, 0);  // a3 0 0
        forearmJoint.localRotation = Quaternion.Euler(0, jointRotations[3], 0);  // 0 a4 0
        wristJoint.localRotation = Quaternion.Euler(jointRotations[4], 0, 0);  // a5 0 0
        handJoint.localRotation = Quaternion.Euler(0, jointRotations[5], 0);  // 0 a6 0

        if (couldSend)
        {
            SendMsg();
        }
    }

    void ThreadReceive()
    {
        if (t != null && t.IsAlive == true)
            return;
        t = new Thread(new ThreadStart(StartReceive));
        t.Start();
    }

    void StartReceive()
    {
        try
        {
            int bufferLen = client.Receive(messageHolder);
            string message = Encoding.UTF8.GetString(messageHolder, 0, bufferLen);
            inMessage.Enqueue(message);
        }
        catch
        {

        }
    }

    void Receive(string message)
    {

        if (message.Contains(","))
        {
            Debug.Log("receive: " + message);
            string[] a1a6 = message.Split(new string[] { "," }, StringSplitOptions.RemoveEmptyEntries);

            float a0 = float.Parse(a1a6[0]);
            float a1 = float.Parse(a1a6[1]);
            float a2 = float.Parse(a1a6[2]);
            float a3 = float.Parse(a1a6[3]);
            float a4 = float.Parse(a1a6[4]);
            float a5 = float.Parse(a1a6[5]);

            // 1: -165~165 / 2: -125~70 / 3: -55~185 / 4: -190~190 / 5: -115~115 / 6: -360~360
            float c0 = ((a0 + 1) / 2) * (165 - (-165)) + (-165);
            float c1 = ((a1 + 1) / 2) * (85 - (-125)) + (-125);
            float c2 = ((a2 + 1) / 2) * (185 - (-55)) + (-55);
            float c3 = ((a3 + 1) / 2) * (190 - (-190)) + (-190);
            float c4 = ((a4 + 1) / 2) * (115 - (-115)) + (-115);
            float c5 = ((a5 + 1) / 2) * (5 - (-5)) + (-5);

            jointRotations[0] = c0;
            jointRotations[1] = c1;
            jointRotations[2] = c2;
            jointRotations[3] = c3;
            jointRotations[4] = c4;
            jointRotations[5] = c5;

            couldSend = true;
        }
        else
        {
            couldSend = true;
            Debug.Log("-------- No data received. --------");
            Disconnect();
        }

    }

    void SendMsg()
    {
        jPosition();
        string posMsg = string.Join(";", axisPositions.Select(p => p.ToString("f8")).ToArray());
        string rotMsg = string.Join(";", jointRotations.Select(r => r.ToString()).ToArray());
        // string message = $"{posMsg};{rotMsg}";
        string message = $"{rotMsg}";

        byte[] data = Encoding.UTF8.GetBytes(message);
        client.Send(data);
        couldSend = false;
        Debug.Log("Sent message: " + message);
    }

    void jPosition()
    {
        baseJoint = GameObject.Find("base_link").transform;
        torsoJoint = GameObject.Find("base_link/upperbase_link/torso_link").transform;

        axisPositions[0] = baseJoint.transform.position - baseJoint.transform.position;  // axis 1 端點: base_link
        axisPositions[1] = torsoJoint.transform.position - baseJoint.transform.position;  // axis 2 端點: torso_link
        axisPositions[2] = shoulderJoint.transform.position - baseJoint.transform.position;  // axis 3 端點: shoulder_link
        axisPositions[3] = armJoint.transform.position - baseJoint.transform.position;  // axis 4 端點: arm_link
        axisPositions[4] = forearmJoint.transform.position - baseJoint.transform.position;  // axis 5 端點: forearm_link
        axisPositions[5] = wristJoint.transform.position - baseJoint.transform.position;  // axis 6 端點: wrist_link
    }

    void Disconnect()
    {
        client.Close();
        t.Abort();
    }
}
