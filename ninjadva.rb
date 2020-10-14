require "yaml"

class NinjaDVA
	def verbose_copy(comment,from,to)
		file_ary = Dir.glob(from)
		FileUtils.cp(file_ary, to)
		verbose_print(comment,file_ary) if @options[:verbose]
	end
	def verbose_delete(comment,files,target_dir)# deletes basename of files(wildcard) in target_dir
		file_ary = Dir.glob(files)
		verbose_print(comment,file_ary) if @options[:verbose]
		file_ary.each{|file|
			file_name = File.basename(file)
			path_to_file = target_dir + file_name
			FileUtils.rm(path_to_file) if File.exist?(path_to_file)
		}
	end
	def verbose_print(headline,file_array)
		puts headline
		file_array.each{|c|
			puts " - #{File.basename(c)}"
		}
	end
	def initialize(config, options = {})
		@options = options
		# set some defaults
		options[:ninjadva_dir] ||= ".."
		options[:challenge_descriptions_dir] ||= "./ninjadva/challenge-descriptions/"
		options[:dashboard_widgets_dir] ||= "./ninjadva/dashboard-widgets/"
		options[:dashboard_admin_widgets_dir] ||= "./ninjadva/dashboard-admin/"
		if config.vm.hostname.class == String
			options[:link_widget_links] ||= [{ hostname: config.vm.hostname, name: config.vm.hostname }]
		else
			options[:link_widget_links] ||= []
		end

		if File.exists?("#{options[:ninjadva_dir]}/.ninjadvarc.yaml")
			ninjadvarc = YAML::load_file("#{options[:ninjadva_dir]}/.ninjadvarc.yaml")
			options[:ssh_key] ||= ninjadvarc["ssh_key"] if ninjadvarc["ssh_key"]
			options[:verbose] ||= ninjadvarc["verbose"] if ninjadvarc["verbose"]
		end
		config.vm.provider "virtualbox" do |vb|
			vb.name = "NinjaDVA_#{ninjadvarc["domain"]}_#{config.vm.hostname}"
		end

		if options[:ssh_key]
			keyfile = "$HOME/.ssh/authorized_keys"
			config.vm.provision "shell", inline: <<-SHELL
				mkdir -p $(dirname #{keyfile})
				touch #{keyfile}
			SHELL
			keys = options[:ssh_key].class == Array ? options[:ssh_key] : [options[:ssh_key]]
			keys.compact.each{|key|
				config.vm.provision "shell", inline: <<-SHELL
					grep --quiet '#{key}' #{keyfile}
					if [ "$?" = 1 ];then
						echo #{key} >> #{keyfile}
						chmod go-rw #{keyfile}
					fi
				SHELL
			}
		end

		# add an interface to the vm that is in the same internal network like the gateway vm
		unless options[:ignore_network_config]
			if options[:mac]
				config.vm.network "private_network", type: "dhcp", virtualbox__intnet: "ninjadva_#{ninjadvarc["domain"]}", mac: options[:mac]
			else
				config.vm.network "private_network", type: "dhcp", virtualbox__intnet: "ninjadva_#{ninjadvarc["domain"]}"
			end
			# change default gw to our own gateway (not the hypervisor)
			config.vm.provision "shell", run: "always", inline: <<-END
				if [ -x /bin/ip ];then
					ip route del default
					ip route add default via 172.23.42.1
				elif [ -x /sbin/ifconfig ];then
					route del default
					route add default gw 172.23.42.1
				fi
			END
		end

		# install ninjadva specific software
		config.vm.provision "shell", inline: <<-END
			if [ -x /usr/bin/apt-get ];then
				apt-get -y update
				apt-get -y install curl
			fi
			if [ -x /usr/bin/pacman ];then
				pacman --noconfirm -S curl
			fi
		END
		config.vm.provision "file", source: "#{options[:ninjadva_dir]}/ninjadva_service", destination: "/tmp/tmp_provision/ninjadva_service"
		config.vm.provision "shell", inline: <<-END
			cd /tmp/tmp_provision/
			cp -R ninjadva_service /usr/share/
			chmod +x /usr/share/ninjadva_service/ninjasolver.sh
			ln -sf /usr/share/ninjadva_service/ninjasolver.sh /usr/local/bin/ninjasolver
			rm -rf *
		END


		# copy challenges and widgets to dashboard, before the vm is started
		config.trigger.after :up do |trigger|
			trigger.info = "Register VM on Dashboard"
			trigger.run = {
				path: "#{options[:ninjadva_dir]}/ninjadva",
				args: [
					"register",
					File.basename(Dir.pwd),
					options[:challenge_descriptions_dir],
					options[:dashboard_widgets_dir],
					options[:dashboard_admin_widgets_dir]
				]
			}
		end

		## add host to list of available favourite links
		options[:link_widget_links].each{|link|
			config.trigger.after :up do |trigger|
				trigger.info = "Register Link: #{link[:hostname]}"
				trigger.run = {
					path: "#{options[:ninjadva_dir]}/ninjadva",
					args: [
						"addlink",
						link[:hostname],
						link[:name]
					]
				}
			end
		}

		# delete all challenges/widgets included in this vm from the dashboard vm
		config.trigger.before [:halt,:destroy] do |trigger|
			trigger.info = "Deregister VM on Dashboard"
			trigger.run = {
				path: "#{options[:ninjadva_dir]}/ninjadva",
				args: [
					"deregister",
					File.basename(Dir.pwd),
					options[:challenge_descriptions_dir],
					options[:dashboard_widgets_dir],
					options[:dashboard_admin_widgets_dir]
				]
			}
		end

		## delete host from list of available favourite links
		options[:link_widget_links].each{|link|
			config.trigger.before [:halt,:destroy] do |trigger|
				trigger.info = "Delete Link: #{link[:hostname]}"
				trigger.run = {
					path: "#{options[:ninjadva_dir]}/ninjadva",
					args: [
						"rmlink",
						link[:hostname],
						link[:name]
					]
				}
			end
		}
	end
end
