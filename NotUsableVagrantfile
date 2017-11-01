#!/usr/bin/ruby

##############################
# NinjaDVA Vagrant manager
##############################

# Place your virtual machines in subdirectories ending with _vm.
# make sure there is a Vagrantfile in each subdir having following structure:

# Vagrant.configure("2") do |config|
# 	config.vm.define "some_unique_vm_name", autostart: false do |config|
# 	  config.vm.hostname = 'some_unique_vm_name'
#     .........
# 	end
# end

# [Hint:]
# Be smart and chose the name of the folder equal to the defined vagrant VM define
# name and the hostname of the VM.

# You can start a specific machine via `vagrant up some_unique_vm_name`.


# Requirements:
# Please execute `vagrant plugin install vagrant-triggers`
# if you start the vm the first time and get an error

puts <<~END
========================================
==========     Ninja DVA      ==========
========================================

END


# search for all Vagrant files in subdirectories ending with "*_vm"
puts "Detected VMs:\n.............\n"
Dir.glob("./*/Vagrantfile").each do|vfile|
	vm_dir = vfile.split("/")[1]
	puts " - " + vm_dir
	abs_path = File.expand_path(vfile, File.dirname(__FILE__))
	$current_vm_path = vm_dir
	load abs_path
end
puts "\n\n"

