import os,sys

class vrunn(object):
    def __init__(self, host:list=[]):
        self.host = host
        self.host_statuses={x:"NONE" for x in self.host}

    def __cmd(self, string):
        print(string)
        try:os.system(string)
        except:pass

    def setup(self):
        for host in self.host:
            self.__cmd("vagrant up {0}".format(host))
            self.host_statuses[host] = "UP"

    def destroy(self):
        for host in self.host:
            self.__cmd("vagrant destroy {0}".format(host))
            self.host_statuses[host] = "NONE"

    def down(self):
        return self.cmd(string="down", prefix=prefix, suffix=suffix)

    def suspend(self):
        return self.cmd(string="suspend", prefix=prefix, suffix=suffix)

    def resume(self):
        return self.cmd(string="resume", prefix=prefix, suffix=suffix)

    def destroy(self, force:bool=True, prefix="", suffix=""):
        if self.do_destroy:
            command = "destroy"
            if force:
                command = command + " -f"
            return self.cmd(command, prefix=prefix, suffix=suffix)
        return None

    def __enter__(self):
        self.up()
        return self

    def __exit__(self, a=None,b=None,c=None):
        self.destroy()
        return

    def run(self, string:str=None, dyr:str="/vagrant", prefix="", suffix=""):
        if dyr:
            string = "cd {0}/;{1}".format(string, dyr)
        return self.cmd(string=string, prefix=prefix, suffix=suffix)

    def trun(self, string:str=None, dyr:str="/vagrant", prefix="", suffix=""):
        return self.cmd(
            string='tmux new-session -d  "{0}"'.format(string),
            dyr=dyr,
            prefix=prefix,
            suffix=suffix
        )