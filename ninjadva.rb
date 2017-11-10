# Requirements:
# Please execute `vagrant plugin install vagrant-triggers`
# if you start a vm importing the first time and get an error
class NinjaDVA
	def initialize(config, options = {})
	    # add a interface to the vm that is in the same internal network like the gateway vm
	    config.vm.network "private_network", type: "dhcp", virtualbox__intnet: "ninjadva"

	    # install ninjadva specific software
	    config.vm.provision "shell", inline: <<~END
		apt-get -y update
		apt-get -y install ruby ruby-dev
		gem install slop
	    END
	    config.vm.provision "file", source: "../ninjadva_service", destination: "/home/vagrant/tmp_provision/ninjadva_service"
	    config.vm.provision "shell", inline: <<~END
		cd /home/vagrant/tmp_provision/
		cp -R ninjadva_service /usr/share/
		chmod +x /usr/share/ninjadva_service/ninjasolver.rb
		ln -sf /usr/share/ninjadva_service/ninjasolver.rb /usr/local/bin/ninjasolver
		rm -rf *
	    END

		
	  # set necessary variables for provision of challenges
	   dashboard_dir = "../dashboard_vm/"
		if !options.key?(:challenge_descriptions_dir)
			options[:challenge_descriptions_dir] = "challenge-descriptions/"
		end

		# check whether dashboard_vm exists
		if Dir.exists?(dashboard_dir)
		  require 'fileutils'

		  # copy challenges to dashboard, before the vm is started
		  config.trigger.before :up do
			  yaml_list = Dir.glob("./" + options[:challenge_descriptions_dir] + "/*.yaml")
			  FileUtils.cp(yaml_list, dashboard_dir + "challenge-descriptions/")
		 end

		# delete all challenges  included in this vm from the dashboard vm
	     config.trigger.after :halt do
			puts "Deleting challenges:"
			Dir.glob("./" + options[:challenge_descriptions_dir] + "/*.yaml").each{|file|
			  file_name = File.basename(file)
			  puts " - " + file_name
			  path_to_file = dashboard_dir + "challenge-descriptions/" + file_name
			  FileUtils.rm(path_to_file) if File.exist?(path_to_file)
			}
		 end
		end
	end
end
