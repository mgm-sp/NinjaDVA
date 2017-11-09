#!/usr/bin/ruby

###############################################################
###############          ninjasolver      #####################
#         Sends a solution to the ninjaDVA dashboard          #
###############################################################

require 'net/http'
require 'uri'
require 'slop'

opts = Slop.parse do |o|
    o.string '-r', '--remote_solution_handler_url', 'url of the solution handler script on the dashboard vm', required: true
    o.string '-i', '--ip_addr', 'ip address of the participant solved the challenge', required: true
    o.string '-c', '--category', 'category of the solution', required: true
    o.integer '-s', '--state', 'state of the challenge', required: true
    o.string '--comment', 'comment for the trainer'
  end

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
