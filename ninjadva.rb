# Requirements:
# Please execute `vagrant plugin install vagrant-triggers`
# if you start a vm importing the first time and get an error
class NinjaDVA
	def initialize(config, options = {})
		# set some defaults
		options[:ninjadva_dir] ||= ".."
		options[:challenge_descriptions_dir] ||= "ninjadva/challenge-descriptions/"
		options[:dashboard_widgets_dir] ||= "ninjadva/dashboard-widgets/"
		options[:link_widget_links] ||= [{ hostname: config.vm.hostname, name: config.vm.hostname }]

		# add a interface to the vm that is in the same internal network like the gateway vm
		config.vm.network "private_network", type: "dhcp", virtualbox__intnet: "ninjadva"

		# install ninjadva specific software
		config.vm.provision "shell", inline: <<~END
			apt-get -y update
			apt-get -y install curl
		END
		config.vm.provision "file", source: "#{options[:ninjadva_dir]}/ninjadva_service", destination: "/tmp/tmp_provision/ninjadva_service"
		config.vm.provision "shell", inline: <<~END
			cd /tmp/tmp_provision/
			cp -R ninjadva_service /usr/share/
			chmod +x /usr/share/ninjadva_service/ninjasolver.sh
			ln -sf /usr/share/ninjadva_service/ninjasolver.sh /usr/local/bin/ninjasolver
			rm -rf *
		END


		# set necessary variables for provision of challenges
		dashboard_dir = "#{options[:ninjadva_dir]}/dashboard_vm/"

		# check whether dashboard_vm exists
		if Dir.exists?(dashboard_dir)
			require 'fileutils'

			# copy challenges and widgets to dashboard, before the vm is started
			config.trigger.before :up do
				chal_list = Dir.glob("./" + options[:challenge_descriptions_dir] + "/*.yaml")
				FileUtils.cp(chal_list, dashboard_dir + "challenge-descriptions/")

				widget_list = Dir.glob("./" + options[:dashboard_widgets_dir] + "/*.html")
				FileUtils.cp(widget_list, dashboard_dir + "dashboard-widgets/")

				# add host to list of available favourite links
				linkfile = "#{dashboard_dir}/dashboard-widgets/available_favourite_links.yaml"
				require "yaml"
				if File.exists?(linkfile)
					currentlinks = YAML::load_file(linkfile)
				else
					currentlinks = []
				end
				currentlinks += options[:link_widget_links]
				currentlinks.uniq!
				File.open(linkfile,"w") {|f| f << currentlinks.to_yaml }
			end

			# delete all challenges/widgets included in this vm from the dashboard vm
			config.trigger.after :halt do
				puts "Deleting challenges:"
				Dir.glob("./" + options[:challenge_descriptions_dir] + "/*.yaml").each{|file|
					file_name = File.basename(file)
					puts " - " + file_name
					path_to_file = dashboard_dir + "challenge-descriptions/" + file_name
					FileUtils.rm(path_to_file) if File.exist?(path_to_file)
				}
				puts "Deleting widgets:"
				Dir.glob("./" + options[:dashboard_widgets_dir] + "/*.html").each{|file|
					file_name = File.basename(file)
					puts " - " + file_name
					path_to_file = dashboard_dir + "dashboard-widgets/" + file_name
					FileUtils.rm(path_to_file) if File.exist?(path_to_file)
				}

				# delete host from list of available favourite links
				linkfile = "#{dashboard_dir}/dashboard-widgets/available_favourite_links.yaml"
				require "yaml"
				if File.exists?(linkfile)
					currentlinks = YAML::load_file(linkfile)
				else
					currentlinks = []
				end
				options[:link_widget_links].each{|link|
					currentlinks.delete(link)
				}
				File.open(linkfile,"w") {|f| f << currentlinks.to_yaml }
			end
		end
	end
end
