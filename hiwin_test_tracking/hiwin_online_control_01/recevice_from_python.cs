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
    class recevice_from_python : recevice_from_pythonBase
    {
        static Socket server;
        static readonly int Robot_ID;
        static void Main(string[] args)
        {
            Movement_handle.OPENconnect();
            Movement_handle.OVSpeed(90); // 整體速度百分比
            Movement_handle.Speed(100, 2200);

            server = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
            server.Bind(new IPEndPoint(IPAddress.Parse("127.0.0.1"), 5055));
            Console.WriteLine("------------- Robot Arm Connected -------------");

            int time_start = HRobot.set_timer_start(Robot_ID, 1);

            int starttime = HRobot.get_timer(Robot_ID, 1);
            Console.WriteLine("starttime" + starttime);

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
                Console.WriteLine(message);
                Console.WriteLine(point.ToString());

                int rectime = HRobot.get_timer(Robot_ID, 1);
                Console.WriteLine("rectime:" + rectime);

                if (message.Contains("?"))
                {
                    string[] a1a6 = message.Split(new string[] { "?" }, StringSplitOptions.RemoveEmptyEntries);

                    double[] a1to6 = new double[6] { Convert.ToDouble(a1a6[0]), Convert.ToDouble(a1a6[1]), Convert.ToDouble(a1a6[2]), 0, 0, 0 };

                    Console.WriteLine("[{0}]", string.Join(", ", a1to6));
                    Movement_handle.RunPosAxis(a1to6.Take(6).ToArray());                    

                    int p2ptime = HRobot.get_timer(Robot_ID, 1);
                    Console.WriteLine("p2ptime:"+ p2ptime);
                }
                else
                {
                    Console.WriteLine("------------- Convert Data is Empty -------------");
                }
            }
        }
    }
}
