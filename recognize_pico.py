# %%
from numpy import empty
from pico_class import PicovoiceDemo
import threading
import time
import rospy
import std_msgs.msg


if __name__=="__main__":
    recognizer=PicovoiceDemo(
                keyword_path='/home/mike/catkin_ws/src/recognition/porcupine/resources/keyword_files/linux/alexa_linux.ppn',
                context_path='/home/mike/Picovoice/street_en_linux_2021-05-19-utc_v1_6_0.rhn',
                # porcupine_library_path=args.porcupine_library_path,
                # porcupine_model_path=args.porcupine_model_path,
                # porcupine_sensitivity=args.porcupine_sensitivity,
                # rhino_library_path=args.rhino_library_path,
                # rhino_model_path=args.rhino_model_path,
                # rhino_sensitivity=args.rhino_sensitivity,
                # output_path=os.path.expanduser(args.output_path) if args.output_path is not None else None).run()
    )

# %%
recognizer.run()
# %%
    # x=threading.Thread(target=recognizer.run,args=())
    # x.daemon=True
    # x.start()
    # # pub = rospy.Publisher('chatter', std_msgs.msg.String, queue_size=10)
    # # rospy.init_node('talker', anonymous=True)
    # # rate = rospy.Rate(10)  # 10h
    # # word_to_publish=''


# %%
