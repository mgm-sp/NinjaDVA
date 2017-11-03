# -*- mode: ruby -*-
# vi: set ft=ruby :

# ninjaDVA Dashboard

Vagrant.configure("2") do |config|

	# deactivate the standard shared folder
	config.vm.synced_folder ".", "/vagrant", disabled:true

	# name and version of vm image
	config.vm.box = "debian/contrib-stretch64"
	config.vm.box_version = "9.1.0"

	config.vm.hostname = "gateway"

	# Interface 1
	config.vm.network "forwarded_port", guest: 3128, host: 3128, host_ip: "0.0.0.0", id: "squid", auto_correct: false
	config.vm.network "forwarded_port", guest: 443, host: 8443, host_ip: "0.0.0.0", id: "openvpn", auto_correct: false

	# Interface 2, VirtualBox internal network
	config.vm.network "private_network", auto_config: false, virtualbox__intnet: "ninjadva"

	# Interface 3, bridged device
	if ARGV[0] == "up"  || ARGV[0] == "reload"
		puts <<~END
				>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
				===        Starting Gateway          ===
				<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

		END
		decision_needed = true
		while decision_needed
			puts "Do you want to bridge a hardware network device to the VM? [y/N]"
			decision_needed = STDIN.gets.chomp
			if decision_needed.downcase == "y"
				config.vm.network "public_network", auto_config: false, use_dhcp_assigned_default_route: false
				# promiscuous mode für Interface 3
				config.vm.provider :virtualbox do |vb|
					vb.customize ["modifyvm", :id, "--nicpromisc3", "allow-all"]
				end
				decision_needed = false
			elsif decision_needed.downcase == "n" || decision_needed.to_s.strip.empty?
				config.vm.network "private_network", auto_config: false, virtualbox__intnet: "somename"
				decision_needed = false
			end
		end
	end


	# define commands that will be executed on the vm after the vm is
	# up and running. This is the right place for software installation.
	config.vm.provision "shell", inline: <<~END
				apt-get -y update
				apt-get -y install inotify-tools dnsmasq psmisc squid3
	END

	########### copy files to vm

	# copy network interfaces definition and hosts file to vm
	config.vm.provision "file", source: "./interfaces", destination: "/home/vagrant/tmp_provision/interfaces"
	config.vm.provision "file", source: "./dnsmasq.conf", destination: "/home/vagrant/tmp_provision/dnsmasq.conf"
	config.vm.provision "file", source: "./squid.conf", destination: "/home/vagrant/tmp_provision/squid.conf"

	# move files to their destination
	config.vm.provision "shell", inline: <<~END
				cd /home/vagrant/tmp_provision/
				install -o root -g root interfaces /etc/network/interfaces
				install -o root -g root dnsmasq.conf /etc/dnsmasq.d/dnsmasq.conf
				install -o root -g root squid.conf /etc/squid/squid.conf
	END

	# reload the network configuration
	config.vm.provision "shell", inline: <<~END
				systemctl restart squid.service
			systemctl restart dnsmasq.service
			ifdown eth0
			ifup eth0
			ifdown eth1
				ifup eth1
				ifdown eth2
				ifup eth2
	END
end
