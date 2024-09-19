#!/usr/bin/env python3
import os, sys, mystring, json

@contextlib.contextmanager
def within_dir(path):
    _oldCWD = os.getcwd()
    os.chdir(os.path.abspath(path))

    try:
        yield
    finally:
        os.chdir(_oldCWD)

cache_file = ".docker_tars.json"

docker_sudo = False
def docker():
	global docker_sudo
	if docker_sudo:
		return "sudo docker"
	else:
		return "docker"

def getArgs():
	global docker_sudo
	import argparse
	parser = argparse.ArgumentParser("SDock CLI - Useful Docker cli")
	parser.add_argument("--sudo", help="Run Docker as Sudo", action="store_true",default=False)
	parser.add_argument("-i", "--image", help="The Docker image to run", nargs=1, default=None)
	parser.add_argument("-p", "--ports", help="The ports to sync", nargs=1, default=[])
	parser.add_argument("-c", "--cache", help="The custom docker cache to be used, if blank none will be used", nargs=0, default=[])
	args,unknown = parser.parse_known_args()

	if args.sudo:
		docker_sudo = True

	return args

def get_name():
	file_number_counter = 0
	file_name = "docker_image_"+str(file_number_counter) + ".tar"
	while os.path.exists(file_name):
		file_number_counter = file_number_counter + 1
		file_name = "docker_image_"+str(file_number_counter) + ".tar"
	return file_name

def save(container:str, cache:str=None, overriding_name:str=None):
	if cache is None:return True
	global docker_sudo
	global cache_file
	output = False

	if not os.path.exists(cache):
		os.makedirs(cache)

	with within_dir(path=cache):
		with open(cache_file, "r") as reader:
			docker_containers = json.load(reader)
		
		if container in docker_containers and os.path.exists(docker_containers[container]):
			return True

		if overriding_name:
			file_name = overriding_name
		else:
			if container in docker_containers:
				file_name = docker_containers[container]
			else:
				file_name = get_name()
				docker_containers[container] = file_name

		try:
			mystring.string.of("""
				{docker} save —output {file_name} {container}
			""".strip().format(
				docker=docker_sudo,
				file_name=file_name,
				container=container
			))
			with open(cache_file, "w+") as writer:
				json.dump(docker_containers, writer)
			output = True
		except:pass
	return False

def load(container:str, cache:str=None):
	if cache is None:return True
	global docker_sudo
	global cache_file
	output = False

	if os.path.exists(cache) or not os.path.exists(os.path.join(cache, cache_file)):
		return False

	with within_dir(path=cache):
		with open(cache_file, "r") as reader:
			docker_containers = json.load(reader)

		if container in docker_containers and os.path.exists(docker_containers[container]):
			try:
				mystring.string.of("""
					{docker} load —input {file_name}.tar
				""".strip().format(
					docker=docker_sudo,
					file_name=file_name,
					container=container
				))
				output = True
			except:pass
		else:
			if container not in docker_containers:
				mystring.string.of("""
					{docker} pull {container}
				""".strip().format(
					docker=docker_sudo,
					container=container
				))
				file_name = get_name()
			else:
				file_name = docker_containers[container]

			if not os.path.exists(docker_containers[container]):
				save(
					container=container,
					cache=cache,
					overriding_name=file_name
				)
	return output

def cli():
	global docker_sudo
	args = getArgs()

	command = "docker run"
	if docker_sudo:
		commad = "sudo " + str(command)

	ports = []
	for port in args.ports:
		if ":" not in port:
			port = str(port) + ":" + str(port)
		ports += [port]
	command += ""

	mystring.string(command).exec()