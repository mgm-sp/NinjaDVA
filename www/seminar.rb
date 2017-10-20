require "time"
require_relative "config_defaults"
class Seminar
	attr_accessor :events
	attr_reader :location, :start
	def initialize(args = {})
		@events = []
		@zone = Time.now.getlocal.zone
		if args[:location]
			@location = args[:location]
			$conf.location = args[:location]
		else
			@location = "Dresden, Germany"
		end

		if args[:start]
			@start = DateTime.parse(args[:start] + @zone)
		else
			@start = DateTime.parse("09:00:00 #{@zone}")
		end
		@current_time = @start
		if args[:title]
			event = {
				:title => args[:title],
				:start => @start.to_date,
				:end => @start.to_date
			}
			event[:file] = args[:file] if args[:file]
			event[:url] = "javascript:chooseMaterial(\"#{args[:file]}\")" if args[:file]
			event[:backgroundColor] = args[:backgroundColor] if args[:backgroundColor]
			@events << event
		end
	end
	def location= location
		@location = location
		$conf.location = location
	end

	def add_lecture args
		event = {
			:title => args[:title] ?  args[:title] : "FIXME: Title required",
			:start => @current_time,
			:end   => (args[:duration] ? @current_time+args[:duration].to_f/24/60 : @current_time+90.0/60/24),
		}
		event[:file] = args[:file] if args[:file]
		event[:url] = "javascript:chooseMaterial(\"#{args[:file]}\")" if args[:file]
		event[:backgroundColor] = args[:backgroundColor] if args[:backgroundColor]
		@current_time = event[:end]
		@events << event
		self
	end
	def add_break args = {}
		if args[:visible]
			add_lecture({:backgroundColor => "#008006"}.merge(args))
		else
			@current_time += args[:duration].nil? ? 30.0/60/24 : args[:duration].to_f/60/24
		end
		self
	end
	def new_day args = {}
		startofday = args[:start].nil? ? @start.strftime("%H:%M:%S") : args[:start]+":00"
		@current_time = DateTime.parse((@current_time+1).strftime("%Y-%m-%d ")+(startofday)+@zone)
		@events[0][:end] = (@current_time+1).to_date
		self
	end

	def to_json
		@events.to_json
	end
	def current_lecture_file
		now = DateTime.now
		@events.each{|e|
			return e[:file] if e[:start] < now && e[:end] > now && e[:file]
		}
		return nil
	end
end


if __FILE__ == $0
	require "pp"
	require_relative ARGV[0]
	$conf.events.events.each{|e|
		puts "#{e[:start].strftime("%F %R")} - #{e[:end].strftime("%F %R")}: #{e[:title]}"
	}
end
