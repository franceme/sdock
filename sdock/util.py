import os, sys, time, subprocess, mystring
from dataclasses import dataclass, field
from datetime import datetime

def install_docker(save_file:bool=False):
	#https://docs.docker.com/engine/install/ubuntu/
	for string in [
		"curl -fsSL https://get.docker.com -o get-docker.sh",
		"sudo sh ./get-docker.sh --dry-run",
		'echo "Done"' if save_file else "echo \"Done\" && rm get-docker.sh"
	]:
		try:
			mystring.string(string).exec()
		except: pass

def cur_dir():
	return '%cd%' if sys.platform in ['win32', 'cygwin'] else '`pwd`'