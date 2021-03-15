from owlready2 import *
import random
import os
import glob


# Import and load the ontology from the owl file
onto = get_ontology("Ontology/MEUS.owl")
onto.load()

commands_list=['goback','gohome','enter']

detect_words=[]

DATA_DIR="Dictionaries_txt"

def clear_dir(dir):
    files = glob.glob(dir+"/*")
    for f in files:
        os.remove(f)

def get_subclasses(top_level):

    class_list = list(top_level.subclasses())

    return class_list


def write_list(class_list):

    class_list = [str(i)[+5:] for i in class_list]


if __name__ == '__main__':
    
    top_level_sub = get_subclasses(owl.Thing)
    print("Top_level", top_level_sub)
    # for classes in Top_level:
    #     for subclass in get_level_names(classes):
    #         print(subclass)
    obj = {}

    obj[str(owl.Thing.name)]=[each.name for each in top_level_sub]
    all_classes = list(onto.classes())

    for subclass in all_classes:
        children = get_subclasses(subclass)

        if children:
            subclass=subclass.name
            children=[each.name for each in children]
            children.extend(commands_list)
            obj[str(subclass)] = children
        else:
            detect_words.append(subclass.name)



    print(obj)
    keys=[]
    
    for o in obj:
        keys.append(o)
        


    print(keys)

    ## Saving data

    clear_dir(DATA_DIR)

    # Dictionaries

    for i in keys:
        set=obj[i]
        file=open("Dictionaries_txt/"+str(i)+".txt","w+")
        for word in set:
            file.write(word+"\n")

    # All words and commands to recognize for the language model
    file=open("Dictionaries_txt/total_list.txt","w+")
    for each in commands_list:
        file.write(each+"\n")

    for each in all_classes:
        file.write(each.name+"\n")

    # All words to detect

    file=open("Check_txt/words_to_detect.txt","w+")

    for each in detect_words:

        file.write(each+"\n")

    # Commands file list

    file=open("Check_txt/special_commands.txt","w+")

    for each in commands_list:

        file.write(each+"\n")
        


    

