require "csv"
class Solution
	def initialize(category,state,comment="")
		File.open($conf.solutiondb,"a"){|f|
			f << [category,$cgi.remote_addr,state,comment,Time.now].to_csv
		}
	end
end
