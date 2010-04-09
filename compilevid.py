#!/usr/bin/python
#Once makerawvid.py runs, this script compiles all images into a single folder
import os, sys, re, subprocess

out_path = "/Users/cisco/Desktop/"

dir_list = os.listdir(out_path)
dir_list.sort()
to_folder = out_path+dir_list[0]
dir_list = dir_list[1:len(dir_list)]

if 0:
	for folder in dir_list:
		from_folder = out_path+folder
		proc = subprocess.Popen(["mv -v "+from_folder+"/*.tif "+to_folder+";rm -rf "+from_folder],
								shell=True,
							   )
		proc.wait()
