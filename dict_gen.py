#!/usr/bin/env python3.8

import unittest
import shutil
import sys
import os
from g2p_seq2seq import g2p
import g2p_seq2seq.g2p_trainer_utils as g2p_trainer_utils
from g2p_seq2seq.g2p import G2PModel
from g2p_seq2seq.params import Params
import glob
import ntpath
import global_var as g

def clear_dir(output_dir):
    files = glob.glob(output_dir+"/*")
    for f in files:
        os.remove(f)


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

MODELDIR = "g2p-seq2seq-model"

DATADIR = g.DICTDIRTXT


#decode_file_path = os.path.abspath("/home/mike/SR_Py/helperScripts/Dictionary(Auto)/Thing.txt")
output_file_path = g.DICTDIR

# print(model_dir)
# params = Params(model_dir, decode_file_path)
# params.hparams = g2p_trainer_utils.load_params(model_dir)
# g2p_model = G2PModel(params, test_path=decode_file_path)
# g2p_model.decode(output_file_path=output_file_path)

clear_dir(output_file_path)

filesIn=glob.glob(DATADIR+"/*")


for filenameIn in filesIn:
    filesOut=filenameIn.split('.')[0]
    fileOut=path_leaf(filesOut)
    input=filenameIn
    output=os.path.join(output_file_path,fileOut+".dic")
    params = Params(MODELDIR, input)
    params.hparams = g2p_trainer_utils.load_params(MODELDIR)
    g2p_model = G2PModel(params, test_path=input)
    g2p_model.decode(output_file_path=output)