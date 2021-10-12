#! /usr/bin/env python3
from owlready2 import *
import random
import os
import glob
import global_var as g
import rospy
import std_msgs.msg as std
from pico_class import PicovoiceDemo
os.chdir(sys.path[0])

with open("Dictionaries_txt/all_words.txt","r") as f:
        all_words=f.read().splitlines()
        f.close
onto = get_ontology(g.ONTODIR)
onto.load()
pub = rospy.Publisher('index', std.Int16, queue_size=10)
all_classes = list(onto.classes())
def callback(word):
    word=word.data
    success=False
    for each in all_words:
        if word==each:
            for each in all_classes:
                for eachcom in each.comment:

                    if word==eachcom:
                        word = each.name
            success=True
            print("WORD IS ",word)
            pub.publish(all_words.index(each))
    
    if success==False:
        print("ERROR: The word ",word," is not in the list")


def listener():
    rospy.init_node('listener_for_word', anonymous=True)

    rospy.Subscriber("chatter_word", std.String, callback)

    rospy.spin()


if __name__=="__main__":
    listener()
    





    