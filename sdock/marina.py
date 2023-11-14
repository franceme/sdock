import os,sys,mystring as mys,docker,hugg.dock as container_storage
from sdock.util import open_port, checkPort

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
        self._remove = False

    @property
    def on(self):
        if not self._on:
            self.container
            self.container.start()

            self._off = False
            self._remove = False

        return self._on

    @property
    def off(self):
        if not self._off:
            self.container.stop()

            self._on = False
            self._off = True

        return self._off

    @property
    def remove(self):
        if not self._remove:
            self.off
            self.container.remove()

            self._remove = True

        return self._remove

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
                remove=self.remove_container,
                working_dir=self.working_dir,
                name=self.name,
                volumes=temp_containers
            )
        return self._container

    def __enter__(self):
        self.on
        return self

    def run(self, string):
        return self(string)

    def storage(self):
        self.on
        return self.container_storage(
            container=self.container,
            working_dir=self.working_dir
        )

    def __call__(self, string):
        exit_code=None;logs = []
        try:
            logs = container.exec_run(
                cmd = string,
                privileged=self.sudo,
                workdir=self.working_dir,
                stderr=True, stdout=True
            )
            for log_itr,log in enumerate(logs):
                if log_itr == 0:
                    try:
                        exit_code = int(log.strip())
                    except:pass
                try:
                    logs += [log.decode("utf-8")]
                except Exception as k:
                    print("Error decoding output line {0}".format(str(log)))

        except Exception as e:
            print(e)
        return exit_code, logs

    def __exit__(self, a,b,c):
        self.off
        if self.remove_container:
            self.remove

        return