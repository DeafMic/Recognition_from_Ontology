#! /usr/bin/env python3

import rospy
import std_msgs.msg as std
import keyboard
import os
import sys
from curtsies import Input
os.chdir(sys.path[0])
pub = rospy.Publisher('index', std.Int16, queue_size=10)
time_start=0
loopnum=0
time_ind=0
ind_arr=[]
times_arr=[5.45, 15, 36, 55.3, 112.7, 152, 162, 
    221, 232, 288.4, 353, 364.7, 416, 427, 479, 500, 
    549.7, 562.1, 577, 628, 649.8, 669.9, 717, 734.17, 784.5, 805, 820]

def callback(time):
    time=time.data
    global loopnum
    global time_start
    global ind_arr
    global times_arr
    global time_ind
    if loopnum==0:

        time_start=time
        # print("start time "+str(time))
    
    loopnum+=1
    # if keyboard.read_key()=='space':
    #    inp=input('Enter needed index as Integer. \n')
       
    #    pub.publish(int(inp))
    time_now=time-time_start
    print("time now " +str(round(time_now,2)))
    if time_now >= times_arr[time_ind]:
        pub.publish(ind_arr[time_ind])
        time_ind=time_ind+1
        # print("index now" + str(time_ind))

    

def listener():
    rospy.init_node('listener_for_bagTime', anonymous=True)

    rospy.Subscriber("time", std.Float64, callback)

    rospy.spin()


if __name__=="__main__":
    words_file=open("Check_txt/recognized_words.txt")
    words_arr=words_file.read().splitlines()
    sett=list(set(words_arr))
    
    for each in words_arr:
        for eachInd in sett:
            if each==eachInd:
                ind_arr.append(sett.index(each))


    listener()