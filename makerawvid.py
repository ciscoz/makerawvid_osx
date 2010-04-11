#!/usr/bin/python
import os, sys, re, subprocess
from optparse import OptionParser

usage = "usage: %prog [options] -f config_file -S start_frame -E end_frame -B bg_path -Q seq_path"

parser = OptionParser(usage=usage)
parser.add_option("-f", type="string", dest="config_file",
                  help="configuration file")
parser.add_option("-S", type="int", dest="start_frame",
                  help="start frame")
parser.add_option("-E", type="int", dest="end_frame",
                  help="end frame")
parser.add_option("-B", type="string", dest="bg_path",
                  help="absolute path to background image")
parser.add_option("-Q", type="string", dest="seq_path",
                  help="absolute path to sequence image")

(options, args) = parser.parse_args()

def drange(start, stop, step):
	if start==stop:
		r=start;
		yield r
	else:
		r = start
		while r <= stop:
			yield r
			r += step

# Making sure we have all we need
#if not options.filename:
#	print "NO FILENAME VALUE GIVEN. GOOD-BYE. \n"
#	sys.exit()
#if not options.start_frame:
#	if not options.start_frame==0.0:
#		print "NO START_FRAME VALUE GIVEN. GOOD-BYE. \n"
#		sys.exit()
#if not options.end_frame and not options.end_frame==0.0:
#	print ("\nEND_FRAME VALUE:=START_FRAME:="+str(options.start_frame))
#	frame_range=drange(options.start_frame,options.start_frame,0)
#else:

if not options.config_file:
	print "NO FILENAME GIVEN \n"
	frame_range=drange(options.start_frame,options.end_frame,delta_frame)	
	bg_path=str(options.bg_path)
	seq_path=str(options.seq_path)
else:
	#read from file
	input = open(options.config_file,'r').readlines()
	start_frame_rx=re.compile("start_frame")
	end_frame_rx=re.compile("end_frame")
	bg_path_rx=re.compile("bg_path")
	seq_path_rx=re.compile("seq_path")
	split_rx = re.compile('\s+')
    # search and replace in file printing to the user changed lines 
	for currentline in input: 
		# if the regexp is found 
		if start_frame_rx.search(currentline): 
			start_frame=split_rx.split(currentline)
			start_frame=start_frame[1]
		if end_frame_rx.search(currentline): 
			end_frame=split_rx.split(currentline)
			end_frame=end_frame[1]
		if bg_path_rx.search(currentline): 
			bg_path=split_rx.split(currentline)
			bg_path=bg_path[1]
		if seq_path_rx.search(currentline): 
			seq_path=split_rx.split(currentline)
			seq_path=seq_path[1]

delta_frame = 10

frame_range=range(int(start_frame),int(end_frame),delta_frame)	

proc = subprocess.Popen(["python changeName.py -f "+options.config_file],
                        shell=True,
                       )
proc.wait()

for frame in frame_range:
	start_frame=str(frame)
	end_frame  =str(frame+delta_frame-1)
	print str(start_frame)+"\t"+end_frame+"\n"

	run_cmd = "\"makevideo("+start_frame+","+end_frame+","\
			  +"\'"+bg_path+"\',"+"\'"+seq_path+"\');quit\""
	print run_cmd

	matl = subprocess.Popen(["./matlab","-nojvm -nosplash -nodisplay -r "+\
							 run_cmd],
							 cwd="/Applications/MATLAB_R2008a/bin/",
							#stdout=subprocess.PIPE,
							#stderr=subprocess.PIPE,
							)
	matl.wait()
	stdout_value = matl.communicate()[0]
	print str(stdout_value)

	#mk_dir = ("Output/FTLE_"+str(options.start_frame)+"_"+str(options.end_frame)
	#		  +"_"+str(delta_frame)+"_"+str(options.int_time)) 
	#proc = subprocess.Popen(["mkdir "+mk_dir+";mv -v Output/*.mat "+mk_dir],
	#						shell=True,
	#					   )
proc = subprocess.Popen(["./compilevid.py"],
                        shell=True,
                       )
proc.wait()
