#!/usr/bin/python
# -*- coding: utf-8-*-
# =======================================================================
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
from pybrain.structure import TanhLayer

# Using NetworkWriter
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
# --------------
import Image
import os
import time
import sys
# --------------
from multiprocessing.dummy import Pool as ThreadPool

############################################################################################
############################################################################################

class AINetBuilder(object):

    # =======================================================================
    def __init__(self, _NET_NEW=False, _NET_NAME="AUTO_NAME_NET.xml", _MAKE_DATA_SET=False, _AUTO_SAVE=False):

        # -----------------------------------------------------------------------
        self._pr_line();
        print("| __init__(self): \n");
        start_time = time.time();
        # -------------------------------------------------------------------
        self._DEBUG                                 = True;
        # -------------------------------------------------------------------
        # ARGS
        self._NET_NEW                               = _NET_NEW;
        self._NET_NAME                              = _NET_NAME;

        self._NET_IN                                = 900; # Image (30px * 30px)
        self._NET_OUT                               = 52; # 26(a-z) + 26(A-Z)
        self._NET_HIDDEN                            = ( (self._NET_IN + self._NET_OUT)/2 +1 ); # (900 + 52) / 2 +1 == ?
        self._NET_MAKE_DATA_SET                     = False; #_MAKE_DATA_SET;

        self._NET_TRAINER                           = None;
        self._NET_LEARNINGS_GRADE                   = 0.002; #                   = 0.00012; # 0.00012 == correct
        self._NET_LEARNINGS_GRADE_CONST             = 0.0002; # 0.00012 == correct
        self._NET_WEIGHTDECAY                       = 0.01;
        self._NET_MOMENTUM                          = 0.75;
        self._NET_VERBOSE                           = True;

        self._NET_AUTO_SAVE                         = True; #_AUTO_SAVE;
        self._MK_AUTO_BAK                           = False;
        # -------------------------------------------------------------------
        # Threading
        self._NET_NUM_OF_THR                        = 2; 
        self._ThreadPool                            = None;

        # -------------------------------------------------------------------
        self._VALIND_COLOR_RANGE                    = 175;
        self._LETTER_ARRAY                          = [];
        self._DATA_SET_DIR                          = "alphabet/";
        self._DATA_SET_FILES_DICT                   = {};
        self.TEXT_BIN_DATA_SET                      = '_DATA_('+self._NET_NAME+').dataset';
        # -----------------------------------------------------------------------
        self._TRAIN_RATE                            = 32**6;
        self._TRACERT                               = 0;
        self._TRACERT_ADDER                         = 0.040;
        self._TRACERT_ARRAY                         = "";
        self._TRACERT_DATA_ARR                      = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51];

        # -----------------------------------------------------------------------
        self._TRACERT_DATA_DICT                     = {

            "a": [  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "b": [-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "c": [-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "d": [-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "e": [-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "f": [-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "g": [-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "h": [-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "i": [-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "j": [-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "k": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "l": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "m": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "n": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "o": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "p": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "q": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "r": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "s": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "t": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "u": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "v": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "w": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "x": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "y": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "z": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],

            "A": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "B": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "C": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "D": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "E": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "F": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "G": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "H": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "I": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "J": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "K": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "L": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "M": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "N": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "O": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "P": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            "Q": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1,-1],
            "R": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1,-1],
            "S": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1,-1],
            "T": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1,-1],
            "U": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1,-1],
            "V": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1,-1],
            "W": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1,-1], 
            "X": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1,-1],
            "Y": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1,  -1],
            "Z": [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  1  ]  

        };
        # -----------------------------------------------------------------------
        # AUTO-METHODS
        print("| Done in: "+str(time.time()-start_time)+'sec');

        #self._InitNet();
        # -----------------------------------------------------------------------

    # =======================================================================
    def _InitNet(self):

        # -----------------------------------------------------------------------
        self._pr_line();
        print("| _InitNet(self): \n");
        start_time = time.time();
        # -----------------------------------------------------------------------
        if self._NET_NAME:
            
            # -----------------------------------------------------------------------
            self._SDS = SupervisedDataSet(900, 52); 

            if self._NET_NEW:

                print('| Bulding new NET: '+self._NET_NAME)
                self._NET = buildNetwork(self._SDS.indim, self._NET_HIDDEN, self._SDS.outdim, bias=True); #,hiddenclass=TanhLayer)
                self._SaveNET();
            else:

                print('| Reading NET from: '+self._NET_NAME)
                self._NET = NetworkReader.readFrom(self._NET_NAME)
            # -----------------------------------------------------------------------
            print('| Making AutoBAK: '+str(self._MK_AUTO_BAK))
            
            if self._MK_AUTO_BAK:
                NetworkWriter.writeToFile(self._NET, self._NET_NAME+".AUTO_BAK.xml");
            # -----------------------------------------------------------------------
            print("| Done in: "+str(time.time()-start_time)+'sec');
            # -----------------------------------------------------------------------

        else:
            
            print('| Unknown NET name: >|'+self._NET_NAME+'|<')
            exit();
        # -----------------------------------------------------------------------


    # =======================================================================
    def _InitDataSet(self):

        self._pr_line();
        print("| _InitDataSet(self): \n");
        start_time = time.time();

        # -----------------------------------------------------------------------
        for woord_dict in os.listdir(self._DATA_SET_DIR):
            self._DATA_SET_FILES_DICT[woord_dict] = woord_dict;
            
        # -----------------------------------------------------------------------
        if self._NET_MAKE_DATA_SET:

            print("| Creating new DataSet: "+self.TEXT_BIN_DATA_SET+" \n");
            FS = open(self.TEXT_BIN_DATA_SET, "w");

            # -------------------------------------------------------------------
            for LTR in self._DATA_SET_FILES_DICT:

                self._LETTER_ARRAY = [];
                _LETTER_SELECTOR_NAME = self._DATA_SET_FILES_DICT[LTR];
                
                # -------------------------------------------------------------------
                _img = Image.open(self._DATA_SET_DIR+_LETTER_SELECTOR_NAME);
                _pix = _img.load()

                _drawing_W = _img.size[0]; #  (900,900)
                _drawing_H = _img.size[1]; # {'dpi': (96,96)}

                # -------------------------------------------------------------------
                _Y = 0;
                _X = 0;

                _line_data_text_bin_str = LTR[0:1]+':';

                while _Y < _drawing_H:
                    while _X < _drawing_W:

                        if(_pix[_X, _Y][0]+_pix[_X, _Y][1]+_pix[_X, _Y][2])/3 < self._VALIND_COLOR_RANGE:
                            
                            self._LETTER_ARRAY.append(1);
                            _line_data_text_bin_str += "1:";
                        else:
                            self._LETTER_ARRAY.append(0);
                            _line_data_text_bin_str += "0:";

                        _X += 1;
                    _Y += 1;
                    _X = 0;
                # -------------------------------------------------------------------
                # Trim last symbol:
                _line_data_text_bin_str = _line_data_text_bin_str[ 0:len(_line_data_text_bin_str)-2 ];

                FS.write(_line_data_text_bin_str+"\n");

                self._SDS.addSample(self._LETTER_ARRAY, self._TRACERT_DATA_DICT[LTR[0:1]])
                if self._DEBUG:
                    print("| >>> self._SDS.addSample(): ", LTR[0:1], LTR[0:10]+' ...');
            # -------------------------------------------------------------------
            # / for
            FS.close();

        # -----------------------------------------------------------------------
        else:

            print("|  Reading DataSet from: '"+self.TEXT_BIN_DATA_SET+"'\n")

            try:

                FS = open(self.TEXT_BIN_DATA_SET, "r");

                for line in FS:
                    line = line.strip()
                    _this_LTR = line[0:1];
                    DATA = line[2:].strip().split(":");

                    self._LETTER_ARRAY = [];

                    for _val in DATA:
                        if _val == "":
                            continue;
                        self._LETTER_ARRAY.append(int(_val));

                    self._SDS.addSample(self._LETTER_ARRAY, self._TRACERT_DATA_DICT[_this_LTR])

                FS.close();

            except Exception as _data_set_io_err:

                print(_data_set_io_err);
                exit();

        # -----------------------------------------------------------------------
        print("|  DataSet: inited in: "+str(time.time()-start_time)+'sec');
        # -----------------------------------------------------------------------


    # =======================================================================
    def _InitNetTrainer(self):

        self._pr_line();
        print("|  _InitNetTrainer(self): \n");
        start_time = time.time();

        # -----------------------------------------------------------------------
        #self._NET_TRAINER = BackpropTrainer(self._NET, self._SDS, verbose=True, learningrate=0.01, momentum=0.5)#, batchlearning=False)#, weightdecay=0.0) 
        #self._NET_TRAINER.trainUntilConvergence(dataset=self._SDS, verbose=True, validationProportion=0.25);
        #self._NET_TRAINER.trainUntilConvergence();#validationProportion=0.25);
        #print(self._NET_TRAINER.trainEpochs(10));
        #print(self._NET_TRAINER.train());

        #self._NET_TRAINER = BackpropTrainer(self._NET, self._SDS, verbose=True, learningrate=0.001, weightdecay=0.01, momentum=0.75); # , batchlearning=False)#, weightdecay=0.0) 

        #self._NET_TRAINER.trainOnDataset(self._SDS,100);
        #NetworkWriter.writeToFile(self._NET, self._NET_NAME)
        #self._NET_TRAINER.trainUntilConvergence(dataset=None, maxEpochs=None, verbose=None, continueEpochs=10, validationProportion=0.25)
        #self._NET_TRAINER.trainOnDataset(self._SDS);
        #self._NET_TRAINER.testOnData(verbose=True)
        #self._NET_TRAINER.trainUntilConvergence(validationProportion=0.01);
        #print(self._NET_TRAINER.trainUntilConvergence(dataset=self._SDS,verbose=True,validationProportion=0.25));

        #self._NET_TRAINER = BackpropTrainer(self._NET,learningrate=0.01, verbose=True);#, momentum=0.5)
        #self._NET_TRAINER.trainOnDataset(self._SDS,50)
        #self._NET_TRAINER.testOnData(verbose=True)
        # -----------------------------------------------------------------------

        self._NET_TRAINER = BackpropTrainer(
            self._NET, self._SDS, 
            verbose=self._NET_VERBOSE, learningrate=self._NET_LEARNINGS_GRADE_CONST, 
            weightdecay=self._NET_WEIGHTDECAY, momentum=self._NET_MOMENTUM
        );

        # -----------------------------------------------------------------------
        print("|  Done in: "+str(time.time()-start_time)+'sec');
        # -----------------------------------------------------------------------



    # =======================================================================
    def _SaveNET(self):

        # -----------------------------------------------------------------------
        try:
            self._pr_line();
            print("|  _SaveNET(self): \n");
            start_time = time.time();

            # -----------------------------------------------------------------------
            new_net_name_tmp = "_"+str(self._TRAIN_RATE)[0:6]+"_"+self._NET_NAME;

            print('|  Saving NET to: '+new_net_name_tmp)
            NetworkWriter.writeToFile(self._NET, new_net_name_tmp);

            print("|  Done in: "+str(time.time()-start_time)+'sec');
        except Exception as _save_err:
            print('|  Unable to save NET: '+str(_save_err));
        # -----------------------------------------------------------------------

    # =======================================================================
    def _MakeLearnStep(self, _thisTHRname):

        self._pr_line();
        print("|  _LearnStep(self, _thisTHRname='"+_thisTHRname+"'): \n");
        start_time = time.time();

        # -----------------------------------------------------------------------
        #self._NET_LEARNINGS_GRADE = 0.00012; # 0.00012 == correct
        #self._NET_LEARNINGS_GRADE = 0.0012; 
        #self._NET_LEARNINGS_GRADE = 0.012; 
        #self._NET_LEARNINGS_GRADE = 0.12; 
        #self._NET_LEARNINGS_GRADE = 0.80; 
        #self._NET_LEARNINGS_GRADE = 1.4;
        #self._NET_LEARNINGS_GRADE = 6.2;
        #self._NET_LEARNINGS_GRADE = 10.2;
        #self._NET_LEARNINGS_GRADE = 20.2;

        # -----------------------------------------------------------------------
        try:
            tr_rate = float(str(self._NET_TRAINER.train()));  
            self._TRAIN_RATE = tr_rate      

            print('| '+_thisTHRname+': '+str(tr_rate));
        except Exception as _err:
            print(' ERR: '+str(_err));
        # -----------------------------------------------------------------------
        """
        exit();


        while self._TRAIN_RATE > self._NET_LEARNINGS_GRADE:

            self._TRAIN_RATE = float(str(self._NET_TRAINER.train()));

            if self._NET_AUTO_SAVE:
                self._SaveNET();

        if self._TRAIN_RATE < self._NET_LEARNINGS_GRADE:
            print('| Network ready.');
        """
        # -----------------------------------------------------------------------
        print('| '+_thisTHRname+" Done in: "+str(time.time()-start_time)+'sec');
        # -----------------------------------------------------------------------

    # =======================================================================
    def _InitThreadTrainer(self):

        self._pr_line();
        print(" _InitThreadTrainer(self): \n");
        start_time = time.time();

        # -----------------------------------------------------------------------
        # Make the Pool of workers
        self._ThreadPool = ThreadPool(self._NET_NUM_OF_THR)

        # -----------------------------------------------------------------------
        print("| Done in: "+str(time.time()-start_time)+'sec');
        # -----------------------------------------------------------------------

    # =======================================================================
    def _Learn(self):

        self._pr_line();
        print(" _Learn(self): \n");
        start_time = time.time();

        # -----------------------------------------------------------------------
        #_list_of_thr_names = [ '_THR_1', '_THR_2', '_THR_3', '_THR_4', '_THR_5', '_THR_6', '_THR_7' ];
        _list_of_thr_names = [ '_THR_1', '_THR_2', '_THR_3', '_THR_4' ];

        """
        _list_of_thr_names = [];

        for x in xrange(0, self._NET_NUM_OF_THR+3):
            _list_of_thr_names.append('_THR_'+str(x));
        """
        # -----------------------------------------------------------------------
        self._ThreadPool.map(self._MakeLearnStep, _list_of_thr_names)

        #close the pool and wait for the work to finish 
        self._ThreadPool.close()
        self._ThreadPool.join()

        # -----------------------------------------------------------------------
        print("| Done in: "+str(time.time()-start_time)+'sec');
        # -----------------------------------------------------------------------

    # =======================================================================
    def _pr_line(self):

        # -----------------------------------------------------------------------
        print('|'+('-'*64)+'|');
        # -----------------------------------------------------------------------

    # =======================================================================

############################################################################################
############################################################################################
if __name__ == '__main__':
    
    _argv = sys.argv;
    # -----------------------------------------------------
    if len(_argv) < 2:
        print('./_buildNetwork <NET-NAME.XML>');
        exit(1);

    # -----------------------------------------------------
    # (self, _NET_NEW=False, _NET_NAME="AUTO_NAME_NET.xml", _MAKE_DATA_SET=False, _AUTO_SAVE=False)
    _AINetBuilder = AINetBuilder(False, _argv[1], False, False);
    _AINetBuilder._InitNet();
    _AINetBuilder._InitDataSet();
    _AINetBuilder._InitNetTrainer();
    #_AINetBuilder._InitThreadTrainer();
    """
    print('|  _AINetBuilder._Learn(): Init');
    _AINetBuilder._Learn();
    print('|  _AINetBuilder._Learn(): Done');
    exit();
    """
    # -----------------------------------------------------
    _C = 0;

    while _AINetBuilder._TRAIN_RATE > _AINetBuilder._NET_LEARNINGS_GRADE:

        print('|  Starting MainWileLoop: '+str(_C));
        _AINetBuilder._InitThreadTrainer();
        _AINetBuilder._Learn();
        _AINetBuilder._SaveNET();

        _C += 1;









