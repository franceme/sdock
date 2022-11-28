import os, sys
from dataclasses import dataclass

@dataclass
class dock:
    """Class for keeping track of an item in inventory."""
    docker: str = "docker"
    ports: list = []
    cmd: str = None
    dind: bool = False
    detach: bool = False
    sudo: bool = False
    mount: str = None
    name: str = "current_running"
    login: bool = False
    loggout: bool = False
    logg: bool = False
    macaddress: str = None


    def string(self):
        if self.dind or self.shared:
            if False and platform.system().lower() == "darwin":  #Mac
                dockerInDocker = "--privileged=true -v /private/var/run/docker.sock:/var/run/docker.sock"
            else: #if platform.system().lower() == "linux":
                dockerInDocker = "--privileged=true -v /var/run/docker.sock:/var/run/docker.sock"
        else:
            dockerInDocker = ""
        
        if self.shared:
            exchanged = "-e EXCHANGE_PATH=" + os.path.abspath(os.curdir)
        else:
            exchanged = ""

        return "{0} run {1} --rm {2} {3} {4} {5} {6} {7} {8} {9}".format(
            docker,
            dockerInDocker,
            '-d' if detatched else '-it',
            -v \"{use_dir}:{mount}\",
            exchanged,
            getPort(ports),
            flags or '',
            '--mac-address ' + str(mac) if mac else '',
            getDockerImage(dockerName,baredocker),
            cmd or ''
        )

    def _str_(self):