using System;
using System.Collections.Generic;
using System.Text;
using SDKHrobot;

namespace hiwin_online_control_01
{
    class Movement_handle
    { 
        static int Robot_ID;
        unsafe static void Main(string[] args)
        {
            Console.WriteLine("Done!!");
            while (true) 
            {
                if(Console.KeyAvailable)
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

        public static unsafe void OPENconnect()
        {
            Robot_ID = HRobot.open_connection("192.168.1.102", 1, Test);  // robot ip 
            HRobot.set_operation_mode(Robot_ID, 1);
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
        public static void OVSpeed(int v)
        {
            HRobot.set_override_ratio(Robot_ID, v); // 整體速度

        }

        unsafe static void Test(ushort cmd, ushort rlt, char* msg, int len)
        {
        }
    }
}
