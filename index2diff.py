#! /usr/bin/env python3
#%%
from owlready2 import *
import random
import os
import glob
import global_var as g
import rospy
import std_msgs.msg as std
from pico_class import PicovoiceDemo
os.chdir(sys.path[0])
onto = get_ontology(g.ONTODIR)
onto.load()
all_classes=list(onto.classes())
pub = rospy.Publisher('Sem_dist', std.Int16, queue_size=10)
# %%
with open("Dictionaries_txt/all_classes.txt","r") as f:
        all_words=f.read().splitlines()
        f.close


# %%
def get_dist(class1,class2):
    anc1=[]
    anc2=[]
    fath1=class1
    fath2=class2
    common_fa=None
    while fath1.is_a:
        anc1.append(fath1)
        fath1=fath1.is_a[0]
    while fath2.is_a:
        anc2.append(fath2)
        fath2=fath2.is_a[0]
    for each1 in anc1:
        for each2 in anc2:
            if each1==each2:
                common_fa=each1
                break
        else:
            continue

        break
    if common_fa:
        return anc1.index(common_fa)+anc2.index(common_fa)
    else:
        return False    
# %%



def callback(words):
   
    ind1=words.data[0]
    ind2=words.data[1]
    
    word1=all_words[ind1]
    word2=all_words[ind2]

    for each in all_classes:
        if each.name == word1:
            class1=each
        if each.name == word2:
            class2=each

    dist=get_dist(class1,class2)
    if (dist):
        pub.publish(dist)


# %%

def listener():
    rospy.init_node('listener_for_index', anonymous=True)

    rospy.Subscriber("Sem_indices", std.Int32MultiArray, callback)

    
    rospy.spin()



if __name__=="__main__":
    listener()