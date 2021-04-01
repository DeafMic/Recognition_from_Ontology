#! /usr/bin/env python3
from os import environ, path
from owlready2 import *
from transitions import Machine
from ast import Str
import math
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import rospy
import pyaudio
import std_msgs.msg
import audioop
import numpy as np
import global_var as g

os.chdir(sys.path[0])

# Params
CHUNK = 128  # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
THRESHOLD = 5000
# The threshold intensity that defines silence
# and noise signal (an int. lower than THRESHOLD is silence).

MODELDIR = g.MODELDIR
DICTDIR = g.DICTDIR
LANGDIR = g.LANGDIR
CHECKDIR = g.CHECKDIR
DICTDIRTXT=g.DICTDIRTXT



# Ontology read and load


# Import and load the ontology from the owl file
onto = get_ontology("Ontology/MEUS.owl")
onto.load()



def get_subclasses(top_level):

    class_list = list(top_level.subclasses())

    return class_list


def get_config(fath_level, config):

    dict = 'all_classes'

    config.set_string('-dict', path.join(DICTDIR, dict+'.dic'))
    #config.set_string('-kws', path.join(MODELDIR,'en-us/lang_models/KWS.list'))

    return config


def get_obj(onto):
    top_level_sub = get_subclasses(owl.Thing)
    obj = {}

    obj[owl.Thing] = [each for each in top_level_sub]
    all_classes = list(onto.classes())

    for subclass in all_classes:
        children = get_subclasses(subclass)

        if children:

            obj[subclass] = children

    return obj


def get_child_from_state(state, transitions):

    children = []

    for each in transitions:
        if state in each[1]:
            children.append(each[0])

    return children


def audio_int(Piece):

    r = math.sqrt(abs(audioop.avg(Piece, 4)))
    #print("Intensity", r)

    return r

def anti_copy(wordInput,to_detect):
    i=0
    bingo=''
    for each in to_detect:
        if each==wordInput:
            i = i+1
            bingo = each
    if i==1:
        return True,bingo

    else:
        return False,bingo



def decode_speech(stream, Decoder):
    
    print("Listening..")
    to_publish = ''
    in_speech_bf = False
    decoder.start_utt()
    while not rospy.is_shutdown() and not to_publish:
        ID = 0.0
        buf = stream.read(CHUNK)
        if buf:

            decoder.process_raw(buf, False, False)
            
            if decoder.get_in_speech() != in_speech_bf:
                in_speech_bf = decoder.get_in_speech()
                if not in_speech_bf:
                    for best, i in zip(decoder.nbest(), range(15)):
                        print("Result", best.hypstr,
                                "model score", best.score)
                    decoder.end_utt()

                    try:
                        to_publish = decoder.hyp().hypstr
                        #ID = WordsArr.index(to_publish)
                        print('\n', 'Result:', to_publish, "model score: ", decoder.hyp(
                        ).best_score, " confidence: ", decoder.hyp().prob)
                    except:
                        print("Not in the list")

                    decoder.start_utt()
                    
        else:
            break

    decoder.end_utt()
    return to_publish





if __name__ == '__main__':
    # Get states and transitions from ontology classes

    with open("Check_txt/words_to_detect.txt","r") as f:
        list_to_detect=f.read().splitlines()
        f.close

    with open(CHECKDIR+"total_list(for lm).txt") as f:
        all_words=f.read().splitlines()
        f.close

    with open(DICTDIRTXT+"all_classes.txt") as f:
        all_classes=f.read().splitlines()
        f.close




    word_to_publish=''



    obj = get_obj(onto)

    states = []
    for o in obj:
        states.append(o)

    # print(states)

    transitions = []
    for each in states[1:]:
        transitions.append([each.name, each.is_a[0].name, each.name])

    states = [each.name for each in states]
    initial = states[0]

    print(states)
    # FSM setup


    FSM = Machine(states=states, transitions=transitions, initial=initial)

    children = get_child_from_state(FSM.state, transitions)

    # ROS setup

    pub = rospy.Publisher('chatter', std_msgs.msg.Int16, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)  # 10h

    # Decoder initial setup

    config = Decoder.default_config()
    config.set_string('-hmm', MODELDIR)
    config.set_string('-logfn', 'shinx.log')
    config.set_string('-lm', LANGDIR+"model.lm")
    config.set_float('-vad_threshold',3.3) #3.5 is good, 3-3.6 good range       
    #config.set_int('-vad_postspeech',40)


    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    state_history=[FSM.state]

    # Main Loop

    while not rospy.is_shutdown():

        word_to_publish=''

        index_to_publish=0

        print("Current state is", FSM.state)

        children = get_child_from_state(FSM.state, transitions)

        config = get_config(FSM.state, config)

        decoder = Decoder(config)

        word = decode_speech(stream, decoder)

        for each in all_classes:
            if word==each:
                word_to_publish=word
    




        
        if word_to_publish:
            print("WORD TO PUBLISH is ",word_to_publish)
    

        
        rate.sleep()    
        
