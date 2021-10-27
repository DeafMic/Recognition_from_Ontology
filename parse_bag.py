import rospy
import std_msgs.msg as std
import keyboard
from curtsies import Input
pub = rospy.Publisher('index', std.Int16, queue_size=10)
time_start=0
loopnum=0

def callback(time):
    time=time.data
    global loopnum
    global time_start
   
    if loopnum==0:

        time_start=time
        print("start time "+str(time))
    
    loopnum+=1
    # if keyboard.read_key()=='space':
    #    inp=input('Enter needed index as Integer. \n')
       
    #    pub.publish(int(inp))
    time_now=str(round(time-time_start,1))
    print("current bag time "+time_now)
    

def listener():
    rospy.init_node('listener_for_bagTime', anonymous=True)

    rospy.Subscriber("time", std.Float64, callback)

    rospy.spin()


if __name__=="__main__":
    listener()