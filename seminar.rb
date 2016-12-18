require "time"
class Seminar
	attr_accessor :events
	attr_reader :location
	def initialize(args = {})
		@events = []
		if args[:location]
			@location = args[:location]
			$conf.location = args[:location]
		else
			@location = "Dresden, Germany"
		end

		if args[:start]
			@start = DateTime.parse(args[:start])
		else
			@start = DateTime.parse("09:00:00")
		end
		@current_time = @start
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
		@current_time = DateTime.parse((@current_time+1).strftime("%Y-%m-%d ")+(startofday))
		self
	end

	def to_json
		@events.to_json
	end
end
