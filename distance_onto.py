from owlready2 import *
import random
import global_var as g


# Import and load the ontology from the owl file
onto = get_ontology(g.ONTODIR)
onto.load()


def get_dist(class1,class2):
    dist=0
    

    return dist

if __name__ == '__main__':
    all_classes=list(onto.classes())

    dist=get_dist(all_classes[2],all_classes[10])

