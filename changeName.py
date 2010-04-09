#!/usr/bin/python
import os, glob, sys, re, subprocess
from optparse import OptionParser

usage = "usage: %prog [options] -f config_file"

parser = OptionParser(usage=usage)
parser.add_option("-f", type="string", dest="config_file",
                  help="configuration file")
(options, args) = parser.parse_args()

if not options.config_file:
    print "NO FILENAME GIVEN \n"
    sys.exit()
else:
    #read from file
    input = open(options.config_file,'r').readlines()
    data_path_rx=re.compile("data_path")
    seq_path_rx=re.compile("seq_path")
    split_rx = re.compile('\s+')
    seq_rx = re.compile(r'[S*\/]')

    # search and replace in file printing to the user changed lines 
    for currentline in input:
        # if the regexp is found 
        if data_path_rx.search(currentline):
            data_path=split_rx.split(currentline)
            data_path="../data/"+data_path[1]+"/"
        if seq_path_rx.search(currentline):
            seq_path=split_rx.split(currentline)
            seq_path=seq_path[1]
            seq_path = seq_rx.split(seq_path)
            seqn = int(seq_path[len(seq_path)-2])
    
    for cam in range(1,4):
        fileName = "C00"+str(cam)+"H001S"+'%(#)04d' % {"#": seqn} 
        pathName = data_path+fileName
        bmpList = glob.glob("./"+data_path+fileName+"/*.bmp") # the glob allows you to use wild cards in the
        frames = len(bmpList)
        for frame_num in range(1,frames+1):
            old_file = pathName+"/"+fileName+'%(#)06d' % {"#": frame_num}+".bmp"
            new_file = pathName+"/"+'%(#)06d' % {"#": frame_num}+".bmp"
            if os.path.exists(old_file):
                print old_file+"->"+new_file
                sys.stdout.flush()
                os.rename(old_file,new_file)
            else:
                print "\rFAILED!",
                print old_file
                sys.stdout.flush()
