require "csv"
class Solution
	def initialize(category,state,comment="")
		File.open($conf.solutiondb,"a"){|f|
			f << [category,ENV['REMOTE_ADDR'],state,comment,Time.now].to_csv
		}
	end
end
