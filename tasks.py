#!/usr/bin/env python3
import os,sys
from invoke import task
from sdock import vagrant as v
import shutil

def run(string):
	print(string);os.system(string)

@task
def gitr(c):
	for x in [
		'git config --global user.email "EMAIL"',
		'git config --global user.name "UserName (pythondev@lite)"'
	]:
		run(x)

@task
def cleanenv(c):
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

@task
def execute(c):
	print("Executing")

@task
def vagrantOne(c):
	path = "temp/"
	if os.path.exists(path):
		shutil.rmtree(path)
		os.mkdir(path)

	os.chdir(path)
	v.vagrant().fullStart()
