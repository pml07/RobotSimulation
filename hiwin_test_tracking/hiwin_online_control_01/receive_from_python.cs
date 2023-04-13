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
using System.IO;

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
            Movement_handle.OVSpeed(100);
            Movement_handle.GetOVEspeed();
            Movement_handle.Speed(30, 1000);
            Movement_handle.SetAcc(0.001);

            var root = Directory.GetCurrentDirectory();
            var dotenv = Path.Combine(root, ".env");
            DotEnv.Load(dotenv);
            
            var server_ip = Environment.GetEnvironmentVariable("HOST_IP");
            var server_port = Environment.GetEnvironmentVariable("HOST_PORT");
            server = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
            server.Bind(new IPEndPoint(IPAddress.Parse(server_ip), Int32.Parse(server_port)));
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
                }
                else
                {
                    Console.WriteLine("------------- Convert Data is Empty -------------");
                }
            }
        }
    }
}