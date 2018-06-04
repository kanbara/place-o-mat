# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "bento/ubuntu-16.04"

  vagrant_root = File.dirname(__FILE__)

  # sync the folder this file is in, so the machine has access to source code
  # and changes are propagated
  config.vm.synced_folder vagrant_root, '/vagrant',
      mount_options: ['dmode=777']

  # Using Flask as a server, which defaultly runs on port 5000
  # deployment here would require more security than this,
  # but for devel purposes it should suffice
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.provider "virtualbox" do |vb|
      # Customize the amount of memory on the VM
      vb.memory = "1024"

      # sync the time between host and guest
      vb.customize ["guestproperty", "set", :id, "/VirtualBox/GuestAdd/VBoxService/--timesync-set-threshold", 1000]
  end

  # shell script that will run setting up things such as packages, pip packages,
  # and operating environment
  config.vm.provision "shell", inline: "/bin/bash /vagrant/init.sh", privileged: false

  config.ssh.forward_agent = true

end
