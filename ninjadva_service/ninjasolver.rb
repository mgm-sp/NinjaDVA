#!/usr/bin/ruby

###############################################################
###############          ninjasolver      #####################
#         Sends a solution to the ninjaDVA dashboard          #
###############################################################

require 'net/http'
require 'uri'
require 'slop'

begin
	opts = Slop.parse() do |o|
		o.string '-r', '--remote_solution_handler_url', '(required) url of the solution handler script on the dashboard vm', required: true
		o.string '-i', '--ip_addr', '(required) ip address of the participant solved the challenge', required: true
		o.string '-c', '--category', '(required) category of the solution', required: true
		o.integer '-s', '--state', '(required) state of the challenge', required: true
		o.string '--comment', '(optional) comment for the trainer'
		o.on '--help', 'show this help message' do
			puts o
			exit
		end
	end
rescue
	puts "Arguments Error: use the --help flag to get more information about the right usage"
	exit 1
end

#puts opts

def send_solve(remote_solution_handler_url, ip_addr, category, state, comment="")
	post_payload = {
		'ip_addr' => ip_addr,
		'category' => category,
		'state' => state,
		'comment' => comment ? comment : ""
	}
	Net::HTTP.post_form(URI.parse(remote_solution_handler_url), post_payload)
end

send_solve(opts[:remote_solution_handler_url], opts[:ip_addr], opts[:category], opts[:state], opts[:comment])
