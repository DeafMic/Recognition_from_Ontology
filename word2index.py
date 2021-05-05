from owlready2 import *
import random
import os
import glob
import global_var as g
import rospy
import std_msgs.msg as std
from pico_class import PicovoiceDemo

global all_words


onto = get_ontology(g.ONTODIR)
onto.load()
with open("Dictionaries_txt/all_classes.txt","r") as f:
        all_words=f.read().splitlines()
        f.close

pub = rospy.Publisher('index', std.Int16, queue_size=10)

def callback(word):
    word=word.data
    
    for each in all_words:
        if word==each:
            
            pub.publish(all_words.index(each))



def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("chatter", std.String, callback)

    # while not rospy.is_shutdown():
    #     if index:
    #         pub.publish(index)
    #     rospy.sleep(1)
    rospy.spin()


if __name__=="__main__":
    listener()
    





    