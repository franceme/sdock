#!/usr/bin/env python3
import os,sys
import shutil
from sdock import vagrant as v

path = "temp/"

def run(string):
	print(string);os.system(string)

def gitr():
	for x in [
		'git config --global user.email "EMAIL"',
		'git config --global user.name "UserName (pythondev@lite)"'
	]:
		run(x)

def cleanenv():
	for x in [
		'CachedExtensions/',
		'CachedExtensionVSIXs/',
		'User/',
		'Machine/',
		'extensions/',
		'logs/',
		'coder.json',
		'machineid',
	]:
		run("yes|rm -r " + str(x))

def execute():
	print("Executing")

def vagrantPatch():
    for x in [
        "sudo gem install fog-libvirt",
        "vagrant plugin install winrm ",
        "vagrant plugin install winrm-elevated"
    ]:
        run(x)

def vagrantOne():
	if os.path.exists(path):
		shutil.rmtree(path)

	os.mkdir(path)
	os.chdir(path)
	v.vagrant().fullStart()

def vagrantClean():
	os.chdir(path)
	v.vagrant().destroy()

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("tasks")
	parser.add_argument("-v","--vagrantOne", action="store_true",default=False, help="Run Vagrant")
	parser.add_argument("-p","--vagrantPatch", action="store_true",default=False, help="Run Vagrant")
	parser.add_argument("-c","--clean", action="store_true",default=False, help="Run Vagrant")
	return parser.parse_args()

if __name__ == '__main__':
	argz = getArgs()
	if argz.vagrantOne:
		vagrantOne()
	elif argz.vagrantPatch:
		vagrantPatch()
	elif argz.clean:
		vagrantClean()
