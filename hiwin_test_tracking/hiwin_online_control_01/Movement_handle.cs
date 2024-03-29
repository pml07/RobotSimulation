﻿using System;
using System.Collections.Generic;
using System.Text;
using SDKHrobot;

namespace hiwin_online_control_01
{
    class Movement_handle
    {
        static int Robot_ID;
        static HRobot.CallBackFun Callbackfunc;

        unsafe static void Main(string[] args)
        {
            Console.WriteLine("Done!!");
            while (true)
            {
                if (Console.KeyAvailable)
                {
                    HRobot.disconnect(Robot_ID);
                }
            }
        }

        public static void RunPTP(double[] targetPOS)
        {
            HRobot.ptp_pos(Robot_ID, 1, targetPOS);  // p2p
        }
        public static void RunLIN(double[] targetPOS)
        {
            HRobot.lin_pos(Robot_ID, 3, 3, targetPOS);  // 直線運動
        }
        public static void RunPosAxis(double[] targetPOS)
        {
            HRobot.ptp_axis(Robot_ID, 1, targetPOS);  // 6axis
        }

        public static void SetAcc(double value)
        {
            HRobot.set_acc_time(Robot_ID, value);  // 加速度時間
        }

        public static unsafe void OPENconnect()
        {
            Callbackfunc = new HRobot.CallBackFun(Test);
            Robot_ID = HRobot.open_connection("192.168.0.103", 1, Callbackfunc);  // robot ip 
            HRobot.set_operation_mode(Robot_ID, 1);
            Console.WriteLine("回傳結果" + Robot_ID);
        }
        public static void DISconnect()
        {
            HRobot.motion_abort(Robot_ID);
            HRobot.disconnect(Robot_ID);
        }

        public static void Speed(int PTP_v, double LIN_v)
        {
            HRobot.set_ptp_speed(Robot_ID, PTP_v);
            HRobot.set_lin_speed(Robot_ID, LIN_v);
        }

        public static void GetOVEspeed()
        {
            HRobot.get_override_ratio(Robot_ID); // 取整體速度
        }

        public static void OVSpeed(int v)
        {
            HRobot.set_override_ratio(Robot_ID, v); // 設定整體速度
        }

        public static void Current_Angles(double[] coor)
        {
            HRobot.get_current_joint(Robot_ID, coor); // degree
        }

        public static void Current_Pos(double[] coor)
        {
            HRobot.get_current_position(Robot_ID, coor); // mm
        }

        public static void Get_timer()
        {
            HRobot.get_timer(Robot_ID, 1);
        }

        public static void Current_rpm(double[] coor) // 馬達轉速
        {
            HRobot.get_current_rpm(Robot_ID, coor);
        }

        public static void Motor_torque(double[] cur)
        {
            HRobot.get_motor_torque(Robot_ID, cur); // 馬達扭力
        }

        public static void Get_alarm_code(ref int count, ulong[] alarm_code)
        {
            HRobot.get_alarm_code(Robot_ID, ref count, alarm_code); // get alarm msg
        }

        public static void Clear_alarm()
        {
            HRobot.clear_alarm(Robot_ID); // clear alarm msg
        }

        unsafe static void Test(ushort cmd, ushort rlt, char* msg, int len) //alarm msg
        {
            switch (cmd)
            {
                case 0:
                    if (rlt == 4030)
                    {
                        Console.WriteLine("HRSS_ALARM_NOTIFY");
                        Console.WriteLine(rlt);
                        Console.WriteLine(cmd);
                        Console.WriteLine(*msg);
                    }
                    else if (rlt == 4031)
                    {
                        Console.WriteLine("HRSS_BATTERY_WARNING");
                        Console.WriteLine(rlt);
                        Console.WriteLine(cmd);
                        Console.WriteLine(*msg);
                    }
                    else if (rlt == 4032)
                    {
                        Console.WriteLine("HRSS_BATTERY_ALARM");
                        Console.WriteLine(rlt);
                        Console.WriteLine(cmd);
                        Console.WriteLine(*msg);
                    }
                    else if (rlt == 4034)
                    {
                        Console.WriteLine("網路通訊訊息");
                        Console.WriteLine(rlt);
                        Console.WriteLine(cmd);
                        Console.WriteLine(*msg);
                    }
                    else if (rlt == 4035)
                    {
                        Console.WriteLine("RS232通訊訊息");
                        Console.WriteLine(rlt);
                        Console.WriteLine(cmd);
                        Console.WriteLine(*msg);
                    }
                    else if (rlt == 4702)
                    {
                        Console.WriteLine("以下資訊改變");
                        Console.WriteLine(rlt);
                        Console.WriteLine(cmd);
                        Console.WriteLine(*msg);
                    }
                    else if (rlt == 4716)
                    {
                        Console.WriteLine("HRSS傳給SDK");
                        Console.WriteLine(rlt);
                        Console.WriteLine(cmd);
                        Console.WriteLine(*msg);
                    }
                    break;
                case 13:
                    Console.WriteLine("連線中斷");
                    Console.WriteLine(rlt);
                    Console.WriteLine(cmd);
                    Console.WriteLine(*msg);
                    break;
                case 1450:
                    switch (rlt)
                    {
                        case 4028:
                            Console.WriteLine("HRSS_START_CLEAR_ALARM");
                            Console.WriteLine(rlt);
                            Console.WriteLine(cmd);
                            Console.WriteLine(*msg);
                            break;
                        case 4029:
                            Console.WriteLine("HRSS_FINISH_CLEAR_ALARM");
                            Console.WriteLine(rlt);
                            Console.WriteLine(cmd);
                            Console.WriteLine(*msg);
                            break;
                        default:
                            break;
                    }
                    break;
                case 4001:
                    switch (rlt)
                    {
                        case 4011:
                            Console.WriteLine("ERROR_OPEN_FILE");
                            Console.WriteLine(rlt);
                            Console.WriteLine(cmd);
                            Console.WriteLine(*msg);
                            break;
                        case 4014:
                            Console.WriteLine("HRSS_TASK_START_FINISH");
                            Console.WriteLine(rlt);
                            Console.WriteLine(cmd);
                            Console.WriteLine(*msg);
                            break;
                        default:
                            break;
                    }
                    break;
                case 4011:
                    switch (rlt)
                    {
                        case 4020:
                            Console.WriteLine("HRSS_UPDATE_FILE_ERROR");
                            Console.WriteLine(rlt);
                            Console.WriteLine(cmd);
                            Console.WriteLine(*msg);
                            break;
                        case 4021:
                            Console.WriteLine("HRSS_UPDATE+FILE_TRANSFER_ERROR");
                            Console.WriteLine(rlt);
                            Console.WriteLine(cmd);
                            Console.WriteLine(*msg);
                            break;
                        case 4022:
                            Console.WriteLine("HRSS_UPDATE_FILE_UNARCHIVER_ERROR");
                            Console.WriteLine(rlt);
                            Console.WriteLine(cmd);
                            Console.WriteLine(*msg);
                            break;
                        case 4023:
                            Console.WriteLine("HRSS_HARD_DISK_CAPACITY_IS_NOT_ENOUGH");
                            Console.WriteLine(rlt);
                            Console.WriteLine(cmd);
                            Console.WriteLine(*msg);
                            break;
                        case 4026:
                            Console.WriteLine("HRSS_START_UPDATE");
                            Console.WriteLine(rlt);
                            Console.WriteLine(cmd);
                            Console.WriteLine(*msg);
                            break;
                        case 4027:
                            Console.WriteLine("HRSS_UPDATE_FILE_TRANSFER_SUCCESS");
                            Console.WriteLine(rlt);
                            Console.WriteLine(cmd);
                            Console.WriteLine(*msg);
                            break;
                        default:
                            break;
                    }
                    break;
                case 4151:
                    Console.WriteLine("手臂資訊");
                    Console.WriteLine(rlt);
                    Console.WriteLine(cmd);
                    Console.WriteLine(*msg);
                    break;
                case 4202:
                    switch (rlt)
                    {
                        case 0:
                            Console.WriteLine("TCPIP success");
                            Console.WriteLine(rlt);
                            Console.WriteLine(cmd);
                            Console.WriteLine(*msg);
                            break;
                        case 9999:
                            Console.WriteLine("TCPIP failed");
                            Console.WriteLine(rlt);
                            Console.WriteLine(cmd);
                            Console.WriteLine(*msg);
                            break;
                        default:
                            break;
                    }
                    break;
                case 4701:
                    Console.WriteLine("API 解析失敗");
                    Console.WriteLine(rlt);
                    Console.WriteLine(cmd);
                    Console.WriteLine(*msg);
                    break;
                default:
                    break;
            }
        }
    }
}
