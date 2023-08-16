using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class Axis_6to6_loader
{
    // joint list define: [j1, j2, j3, j4, j5, j6]
    public static string coordinate_txt_path = @"Assets/DataSet/Demo/6to6_demo/gt_rot_demo.txt";
    public static string[] coordinate_lines = File.ReadAllLines(coordinate_txt_path);
    public static float[,] coordinate_list = new float[coordinate_lines.Length, 6];

    public void txt_reader()
    {
        int count = 0;
        foreach (var item in coordinate_lines)
        {
            string[] subs = item.Split(',');
            coordinate_list[count, 0] = (float)Convert.ToDouble(subs[0]);
            coordinate_list[count, 1] = (float)Convert.ToDouble(subs[1]);
            coordinate_list[count, 2] = (float)Convert.ToDouble(subs[2]);
            coordinate_list[count, 3] = (float)Convert.ToDouble(subs[3]);
            coordinate_list[count, 4] = (float)Convert.ToDouble(subs[4]);
            coordinate_list[count, 5] = (float)Convert.ToDouble(subs[5]);
            Debug.Log("---------------");
            Debug.Log(coordinate_list[count, 0] + "," + coordinate_list[count, 1] + "," + coordinate_list[count, 2] + "," + coordinate_list[count, 3] + "," + coordinate_list[count, 4] + "," + coordinate_list[count, 5]);
            
            count += 1;
        }
        count = 0;   
    }
}
