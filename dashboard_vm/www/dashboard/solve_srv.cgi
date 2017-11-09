#!/usr/bin/ruby

# please make sure that this cgi is only available from the vbox internal shared network
# adapt the part in the vhhost.conf accordingly

require 'cgi'
require "csv"
require_relative "../config_defaults"

cgi = CGI.new
puts cgi.header

# terminate if this script is not called via POST method
if cgi.request_method != "POST"
    exit
end

# define method to add a solution
def add_solution(category, ip_addr, state, comment="")
    File.open($conf.solutiondb,"a"){|f|
        f << [category,ip_addr,state,comment,Time.now].to_csv
    }
end

ip_addr = cgi['ip_addr']
category = cgi['category']
state = cgi['state']
comment = cgi['comment']

# terminate if a necessary information is not in place
if (ip_addr.to_s.strip.empty? || category.to_s.strip.empty? || state.to_s.strip.empty?)
    exit
end

# if everything is alright, add the line to the file
add_solution(category, ip_addr, state, comment)
