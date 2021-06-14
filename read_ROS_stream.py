#! /usr/bin/env python3
from owlready2 import *
import random
import os
import glob
import global_var as g
import rospy
import std_msgs.msg as std
from pico_class import PicovoiceDemo
from audio_common_msgs.msg import AudioData
import pyaudio
from picovoice import Picovoice
import wave
os.chdir(sys.path[0])


def callback(data):
    pa = pyaudio.PyAudio()




def listener():
    rospy.init_node('read_stram', anonymous=True)

    rospy.Subscriber("/audio/audio", AudioData, callback)

    rospy.spin()


    


if __name__=="__main__":

    recognizer=PicovoiceDemo(
                    keyword_path='/home/mike/catkin_ws/src/recognition/porcupine/resources/keyword_files/linux/alexa_linux.ppn',
                    context_path='/home/mike/Picovoice/SLAM_en_linux_2021-06-19-utc_v1_6_0.rhn',
                    # porcupine_library_path=args.porcupine_library_path,
                    # porcupine_model_path=args.porcupine_model_path,
                    # porcupine_sensitivity=args.porcupine_sensitivity,
                    # rhino_library_path=args.rhino_library_path,
                    # rhino_model_path=args.rhino_model_path,
                    # rhino_sensitivity=args.rhino_sensitivity,
                    # output_path=os.path.expanduser(args.output_path) if args.output_path is not None else None).run()
        )

    listener()
    