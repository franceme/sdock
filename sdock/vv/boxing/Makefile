vm_name=

#VBoxManage list vms
uuid=

clean:
	-VBoxManage controlvm $(vm_name) acpipowerbutton
	-yes|rm -r .vagrant/
	-vagrant destroy -f
	-rm $(vm_name)_name.box

stash:clean
	vagrant package --base $(uuid) --output $(vm_name).box

load:stash
	vagrant box add $(vm_name)_name $(vm_name).box

run: clean load

#https://oracle-base.com/articles/vm/create-a-vagrant-base-box-virtualbox