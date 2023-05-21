using System;
using System.Linq;
using System.IO;
using WebSocketSharp;
using System.Text.RegularExpressions;
using Newtonsoft.Json;
namespace hiwin_online_control_01
{
    class Receive_from_python
    {
        static WebSocket ws;

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

            ws = new WebSocket($"ws://{server_ip}:{server_port}");
            ws.OnMessage += OnMessage;
            ws.Connect();
            Console.WriteLine("------------- Robot Arm Connected -------------");
            while (true)
            {

                if (Console.KeyAvailable)
                {
                    Movement_handle.DISconnect();
                    ws.Close();
                    Console.WriteLine("------------- Disconnected and Exit -------------");
                    return;
                }
            }
        }

        static void OnMessage(object? sender, MessageEventArgs e)
        {
            // TODO
            int refCount = 0;
            ulong[] alarmCode = new ulong[20];
            Movement_handle.Get_alarm_code(ref refCount, alarmCode);
            
            string alarmValue = alarmCode.ToString();
            Console.WriteLine(alarmValue);
            if (alarmValue.Length == 16) 
            {
                string[] digits = Regex.Split(alarmValue, @"[0-9]{4}}");
                Console.WriteLine(digits[0]);

                if (digits[0] == "0000")
                {
                    Console.WriteLine("------------- Alarm Code is 0000 -------------");
                }
                else
                {
                    Console.WriteLine("------------- Alarm Code is not 0000 -------------");
                    string alarm_code = digits[0];
                    var data = new
                    {
                        alarm_code
                    };

                    string jsonData = JsonConvert.SerializeObject(data);
                    ws.Send(jsonData);
                    return;
                }
            }
            else
            {
                Console.WriteLine("------------- Alarm Code is not 16 digits -------------");
            }

            Console.WriteLine("------------- WebSocket OnMessage -------------");
            string message = e.Data.ToString();
            Console.WriteLine(message);
            if (message.Contains(";"))
            {
                string[] a1a6 = message.Split(new string[] { ";" }, StringSplitOptions.RemoveEmptyEntries);
                double[] a1to6 = new double[6] { Convert.ToDouble(a1a6[0]), Convert.ToDouble(a1a6[1]), Convert.ToDouble(a1a6[2]), Convert.ToDouble(a1a6[3]), Convert.ToDouble(a1a6[4]), Convert.ToDouble(a1a6[5]) };

                Console.WriteLine("[{0}]", string.Join(", ", a1to6));
                Movement_handle.RunPosAxis(a1to6.Take(6).ToArray());

                double[] jointAngles = new double[6];
                Movement_handle.Current_Angles(jointAngles);
                double[] jointPos = new double[6];
                Movement_handle.Current_Pos(jointPos);
                double[] rpms = new double[6];
                Movement_handle.Current_rpm(rpms);
                double[] torqueValues = new double[6];
                Movement_handle.Motor_torque(torqueValues);

                var data = new
                {
                    jointAngles,
                    jointPos,
                    rpms,
                    torqueValues
                };

                string jsonData = JsonConvert.SerializeObject(data);
                ws.Send(jsonData);
            }
            else if(message == "clear_alarm")
            {
                Console.WriteLine("------------- Clear Alarm Message -------------");
                Movement_handle.Clear_alarm();
            }
            else
            {
                Console.WriteLine("------------- Convert Data is Empty -------------");
            } 
        }
    }
}