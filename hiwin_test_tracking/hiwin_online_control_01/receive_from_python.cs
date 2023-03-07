using System;
using System.Collections.Generic;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Linq;
using System.Threading.Tasks;
using System.Threading;
using System.Collections;
using SDKHrobot;

namespace hiwin_online_control_01
{
    class Receive_from_python
    {
        static Socket server;
        static Socket client;
        static readonly int Robot_ID;
        static void Main(string[] args)
        {
            Movement_handle.OPENconnect();
            Movement_handle.OVSpeed(95);
            Movement_handle.GetOVEspeed();
            Movement_handle.Speed(100, 2200);
            server = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
            server.Bind(new IPEndPoint(IPAddress.Parse("127.0.0.1"), 5065));
            Console.WriteLine("------------- Robot Arm Connected -------------");

            client = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);

            Thread t = new Thread(ReceiveMsg);
            t.Start();
        }

        static void ReceiveMsg()
        {
            while (true)
            {
                
                if (Console.KeyAvailable)
                {
                    Movement_handle.DISconnect();
                    Console.WriteLine("------------- Disconnected and Exit -------------");
                    return;
                }

                EndPoint point;
                try
                {
                     point = new IPEndPoint(IPAddress.Any, 0);
                }
                catch (System.ExecutionEngineException)
                {
                    Console.WriteLine("Wrong message from server");
                    continue;
                }

                
                byte[] buffer = new byte[1024];
                int length = server.ReceiveFrom(buffer, ref point);

                string message = Encoding.UTF8.GetString(buffer, 0, length);
                //Console.WriteLine(message);
                //Console.WriteLine(point.ToString());

                if (message.Contains(";"))
                {
                    string[] a1a6 = message.Split(new string[] { ";" }, StringSplitOptions.RemoveEmptyEntries);
                    double[] a1to6 = new double[6] { Convert.ToDouble(a1a6[0]), Convert.ToDouble(a1a6[1]), Convert.ToDouble(a1a6[2]), Convert.ToDouble(a1a6[3]), Convert.ToDouble(a1a6[4]), Convert.ToDouble(a1a6[5]) };

                    Console.WriteLine("[{0}]", string.Join(", ", a1to6));
                    Movement_handle.RunPosAxis(a1to6.Take(6).ToArray());

                    SendMsg();
                }
                else
                {
                    Console.WriteLine("------------- Convert Data is Empty -------------");
                }
            }
        }

        static void SendMsg()
        {
            double[] jointAngles = new double[6];
            Movement_handle.Current_Angles(jointAngles);
            double[] jointPos = new double[6];
            Movement_handle.Current_Pos(jointPos);
            double[] rpms = new double[6];
            Movement_handle.Current_rpm(rpms);
            double[] torqueValues = new double[6];
            Movement_handle.Motor_torque(torqueValues);

            string rotMsg = string.Join(";", jointAngles.Select(r => r.ToString()).ToArray());
            string posMsg = string.Join(";", jointPos.Select(p => p.ToString()).ToArray());
            string rpmMsg = string.Join(";", rpms.Select(rp => rp.ToString()).ToArray());
            string torMsg = string.Join(";", torqueValues.Select(t => t.ToString()).ToArray());
            string message = $"{rotMsg};{posMsg};{rpmMsg};{torMsg}";

            byte[] buffer = Encoding.UTF8.GetBytes(message);
            client.SendTo(buffer, new IPEndPoint(IPAddress.Parse("127.0.0.1"), 5066));
        }
    }
}
