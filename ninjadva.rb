class NinjaDVA
	def initialize(config, options = {})
	  # set necessary variables
	   dashboard_dir = "../dashboard_vm/"
		if !options.key?(:challenge_descriptions_dir)
			options[:challenge_descriptions_dir] = "challenge-descriptions/"
		end

		# check whether dashboard_vm exists
		if Dir.exists?(dashboard_dir)
		  require 'fileutils'

		  # copy tasks to dashboard, before the vm is started
		  config.trigger.before :up do
			  yaml_list = Dir.glob("./" + options[:challenge_descriptions_dir] + "/*.yaml")
			  FileUtils.cp(yaml_list, dashboard_dir + "challenge-descriptions/")
		 end

		# delete all challanges  included in this vm from the dashboard vm
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
