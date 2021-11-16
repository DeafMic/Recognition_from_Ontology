#! /usr/bin/env python3

import argparse
import os
import struct
import sys
from threading import Thread, current_thread

import numpy as np
import pyaudio
import soundfile
from picovoice import Picovoice
import rospy
import std_msgs.msg

class PicovoiceDemo(Thread):
    current_word=None
    understood=None
    pub=rospy.Publisher('chatter_word', std_msgs.msg.String, queue_size=10)
    rate=None
    def __init__(
            self,
            keyword_path,
            context_path,
            porcupine_library_path=None,
            porcupine_model_path=None,
            porcupine_sensitivity=0.5,
            rhino_library_path=None,
            rhino_model_path=None,
            rhino_sensitivity=0.5,
            output_path=None):
        super(PicovoiceDemo, self).__init__()

        self._picovoice = Picovoice(
            keyword_path=keyword_path,
            wake_word_callback=self._wake_word_callback,
            context_path=context_path,
            inference_callback=self._inference_callback,
            porcupine_library_path=porcupine_library_path,
            porcupine_model_path=porcupine_model_path,
            porcupine_sensitivity=porcupine_sensitivity,
            rhino_library_path=rhino_library_path,
            rhino_model_path=rhino_model_path,
            rhino_sensitivity=rhino_sensitivity)

        self.output_path = output_path
        self.current_word=''
        self.understood=False
        self.pub = rospy.Publisher('chatter_word', std_msgs.msg.String, queue_size=10)
        rospy.init_node('word_publisher', anonymous=True)
        self.rate = rospy.Rate(10)  # 10h

        if self.output_path is not None:
            self._recorded_frames = list()

    @staticmethod
    def _wake_word_callback():
        print('[wake word]\n')

    @classmethod
    def _inference_callback(self,inference):
        if inference.is_understood:
            

            print('{')
            print("  intent : '%s'" % inference.intent)
            print('  slots : {')
            for slot, value in inference.slots.items():
                self.pub.publish(value)
                print("    %s : '%s'" % (slot, value))
            print('  }')
            print('}\n')
            
        else:
            print("Didn't understand the command.\n")

    def run(self):
        pa = None
        audio_stream = None

        try:
            pa = pyaudio.PyAudio()

            audio_stream = pa.open(
                rate=self._picovoice.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self._picovoice.frame_length)

            print('[Listening ...]')

            while not rospy.is_shutdown():
                self.understood=False
                pcm = audio_stream.read(self._picovoice.frame_length)                
                pcm = struct.unpack_from("h" * self._picovoice.frame_length, pcm)

                if self.output_path is not None:
                    self._recorded_frames.append(pcm)
                self.understood=False
                self._picovoice.process(pcm)
                #self.rate.sleep()
        except KeyboardInterrupt:
            sys.stdout.write('\b' * 2)
            print('Stopping ...')
        finally:
            if audio_stream is not None:
                audio_stream.close()

            if pa is not None:
                pa.terminate()

            if self.output_path is not None and len(self._recorded_frames) > 0:
                recorded_audio = np.concatenate(self._recorded_frames, axis=0).astype(np.int16)
                soundfile.write(
                    self.output_path,
                    recorded_audio,
                    samplerate=self._picovoice.sample_rate,
                    subtype='PCM_16')

            self._picovoice.delete()

    @classmethod
    def show_audio_devices(cls):
        fields = ('index', 'name', 'defaultSampleRate', 'maxInputChannels')

        pa = pyaudio.PyAudio()

        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            print(', '.join("'%s': '%s'" % (k, str(info[k])) for k in fields))

        pa.terminate()

    @classmethod
    def get_word(self):
       
        return self.current_word
        
             
    @classmethod
    def get_understood(self):
        return self.understood


if __name__=="__main__":
    recognizer=PicovoiceDemo(
                    keyword_path='/home/mike/catkin_ws/src/recognition/porcupine/resources/keyword_files/linux/hey siri_linux.ppn',
                    context_path='/home/mike/Picovoice/SLAM_en_linux_2021-12-03-utc_v1_6_0.rhn',
                    # porcupine_library_path=args.porcupine_library_path,
                    # porcupine_model_path=args.porcupine_model_path,
                    # porcupine_sensitivity=args.porcupine_sensitivity,
                    # rhino_library_path=args.rhino_library_path,
                    # rhino_model_path=args.rhino_model_path,
                    # rhino_sensitivity=args.rhino_sensitivity,
                    # output_path=os.path.expanduser(args.output_path) if args.output_path is not None else None).run()
        )
    recognizer.run()