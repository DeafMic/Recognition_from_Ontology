from owlready2 import *
import random
import os
import glob
import global_var as g

# Import and load the ontology from the owl file


#All words without special commands
def run():
    onto = get_ontology(g.ONTODIR)
    onto.load()

    all_classes = list(onto.classes())
    file=open(g.CHECKDIR+"all_words.txt","w+")
    filePic=open(g.CHECKDIR+"for_pico.txt","w+")
    for each in all_classes:

        filePic.write("      - "+each.name.replace("_"," ")+"\n")
        file.write(each.name.replace("_"," ")+"\n")
        for eachcom in each.comment:
            file.write(eachcom.replace("_"," ")+"\n")
            filePic.write("      - "+eachcom.replace("_"," ")+"\n")


if __name__ == '__main__':
    run()






















# detect_words=[]

# DATA_DIR="Dictionaries_txt"


# def clear_dir(dir):
#     files = glob.glob(dir+"/*")
#     for f in files:
#         os.remove(f)

# def get_subclasses(top_level):

#     class_list = list(top_level.subclasses())

#     return class_list


# def write_list(class_list):

#     class_list = [str(i)[+5:] for i in class_list]


# if __name__ == '__main__':
    
#     top_level_sub = get_subclasses(owl.Thing)
#     print("Top_level", top_level_sub)
#     # for classes in Top_level:
#     #     for subclass in get_level_names(classes):
#     #         print(subclass)
#     obj = {}

#     obj[str(owl.Thing.name)]=[each.name for each in top_level_sub]
#     all_classes = list(onto.classes())

#     for subclass in all_classes:
#         children = get_subclasses(subclass)

#         if children:
#             subclass=subclass.name
#             children=[each.name for each in children]
      
#             obj[str(subclass)] = children
#         else:
#             detect_words.append(subclass.name)



#     print(obj)
#     keys=[]
    
#     for o in obj:
#         keys.append(o)
        


#     print(keys)

#     ## Saving data

#     clear_dir(DATA_DIR)
#     clear_dir(g.CHECKDIR)

#     # Dictionaries

#     for i in keys:
#         set=obj[i]
#         file=open(g.DICTDIRTXT+str(i)+".txt","w+")
#         for word in set:
#             file.write(word+"\n")

#     # All words and commands to recognize for the language model
   

#     for each in all_classes:
#         file.write(each.name+"\n")

#     # All words to detect

#     file=open(g.CHECKDIR+"words_to_detect.txt","w+")

#     for each in detect_words:

#         file.write(each+"\n")



    

#     #All words without special commands
#     file=open(g.DICTDIRTXT+"all_classes.txt","w+")
#     for each in all_classes:
        
#         file.write(each.name.replace("_"," ")+"\n")
        
        


    

