import os,sys,mystring as mys,docker
from sdock.util import open_port, checkPort
from hugg import dock as container_storage

def kill_container(name):
    try:os.system("docker rm -f -v {0}".format(self._name))
    except Exception as e:pass #print("1:Killing")
    
    try:os.system("docker rm -v {0}".format(self._name))
    except Exception as e:pass #print("2:Killing")
    
    try:os.system("docker rm -f {0}".format(self._name))
    except Exception as e:pass #print("3:Killing")
    
    try:os.system("docker rm {0}".format(self._name))
    except Exception as e:pass #print("4:Killing")

class mooring(object):
    def __init__(self, image:str, working_dir:str, ports=[], network=None,detach=False,sudo=True,remove_container=True,name=None,mount_from_to={}):
        self.client = docker.from_env()

        self.image = image
        self.working_dir = working_dir
        self.ports = ports
        self.network = network
        self.detach = detach
        self.sudo = sudo
        self.remove_container = remove_container
        self.name = name
        self.mount_from_to = mount_from_to

        self._container = None
        self._on = False
        self._off = True
        self._remove = True

    @property
    def on(self):
        if not self.is_on():
            try:
                self.container
                self.container.start()
            except Exception as e:
                print("Starting")
                print(e)

            self._on = self.status != "NotCreated"
            self._off = self.status == "NotCreated"
            self._remove = self.status == "NotCreated"

        return self._on

    def is_on(self):
        return self._on

    @property
    def off(self):
        if not self.is_off():
            try:
                self.container.stop()
            except Exception as e:
                print("Stopping")
                print(e)

            self._on = False
            self._off = True

        return self._off

    def is_off(self):
        return self._off

    @property
    def remove(self):
        if not self.is_removed():
            self.off
            try:self.container.kill()
            except Exception as e:print("1:Killing")
            
            try:self.container.remove()
            except Exception as e:print("2:Killing")
            
            try:os.system("docker rm {0}".format(self._name))
            except Exception as e:print("2:Killing")

            self._remove = True

        return self._remove

    def is_removed(self):
        return self._remove

    @property
    def status(self):
        return "NotCreated" if self._container is None else self._container.status

    @property
    def container(self):
        if self._container is None:
            temp_containers = {}
            for mount_from, mount_to_in_container in self.mount_from_to.items():
                temp_containers[mount_from]={
                    "bind":mount_to_in_container,
                    "mode":"rw"
                }

            self._container = self.client.containers.create(
                image = self.image,
                command = "sleep 100000", #Seems to be necessary to keep the container alive while working with it?
                ports = {"{0}/tcp".format(port):port if checkPort(port) else open_port() for port in self.ports}, #Need to fix this
                network=self.network,
                detach=self.detach,
                privileged=self.sudo,
                #user=user_id,
                working_dir=self.working_dir,
                name=self.name,
                volumes=temp_containers
            )

            self.name = self._container.name
        return self._container

    def __enter__(self):
        self.on
        return self

    def run(self, string):
        return self(string)

    def storage(self):
        self.on
        return container_storage(
            container=self.container,
            working_dir=self.working_dir
        )

    def __call__(self, string):
        exit_code=None;output_logs = []
        try:
            logs = self.container.exec_run(
                cmd = string,
                privileged=self.sudo,
                workdir=self.working_dir,
                stderr=True, stdout=True
            )
            for log_itr,log in enumerate(logs):
                if log_itr == 0:
                    try:
                        exit_code = int(str(log))
                    except Exception as e:
                        print("Error decoding {1} @ line {0}".format(str(log_itr), str(log)))
                else:
                    try:
                        log_line = str(log.decode("utf-8")).strip()
                        for subline in log_line.split("\n"):
                            output_logs += [str(subline).strip()]
                    except Exception as k:
                        print("Error decoding {1} @ line {0}".format(str(log_itr), str(log)))

        except Exception as e:
            print(e)
        return exit_code, output_logs

    def __exit__(self, a,b,c):
        self.off
        if self.remove_container:
            self.remove

        return