import gdb
import weakref

class CounterBreakpoint(gdb.Breakpoint):
	def __init__(self, spec):
		super(CounterBreakpoint, self).__init__(spec, gdb.BP_BREAKPOINT, internal = False)
		self.counter = 0
		self.goal = -1

	def stop(self):
		self.counter=self.counter+1
		print("Counter Breakpoint hit: id=", self.number, ", count=", self.counter)
		if (self.goal > 0 and self.counter >= self.goal):
			print("Counter breakpoint ", self.number, " stop")
			return True
		return False

class CountAndBreak(gdb.Command):
	def __init__(self):
		super(CountAndBreak, self).__init__('cb', gdb.COMMAND_DATA, gdb.COMPLETE_SYMBOL)
		self.breakpoints = {}

	def clear(self, bid = -1):
		if (bid >= 0):
			if not bid in self.breakpoints.keys():
				print("There is no counter breakpoint with id:", bid)
				self.show()
			elif self.breakpoints[bid].is_valid():
				print("Clear the counter of breakpoint ", bid, " from ", self.breakpoints[bid].counter, " to 0.")
				self.breakpoints[bid].counter = 0
			else:
				print("Breakpoint ", bid, " seems to be removed, untrack its counter.")
				self.breakpoints.pop(bid, None)
		else:
			print("Clear all breakpoint counters:")
			for bid, breakpoint in self.breakpoints.items():
				print("Clear the counter of breakpoint ", bid, " from ", breakpoint.counter, " to 0.")
				breakpoint.counter = 0

	def show(self):
		print("Current counter breakpoints:")
		for bid, breakpoint in self.breakpoints.items():
			print("Counter breakpoint ", bid, " at ", breakpoint.location)

	def setGoal(self, bid, count = -1):
		if not bid in self.breakpoints.keys():
			print("There is no counter breakpoint with id:", bid)		
		elif (count == -1):
			print("Clear the counter target of breakpoint ", bid, " (was ", self.breakpoints[bid].goal, ")")
			self.breakpoints[bid].goal = -1
		else:
			print("Clear set the counter target of breakpoint ", bid, " to ", count, "(was ", self.breakpoints[bid].goal, " )")
			self.breakpoints[bid].goal = count

	def invoke(self, arg, from_tty):
		args = gdb.string_to_argv(arg)
		if args[0] == "set" or args[0] == "s":
			newBreak = CounterBreakpoint(args[1])
			self.breakpoints[newBreak.number] = newBreak
			self.show()
		elif args[0] == "clear" or args[0] == "c":
			if (len(args) == 2):
				bid = int(args[1])
				print(bid)
				self.clear(bid)
			elif len(args) == 1 or args[1] == "all":
				self.clear()
		elif args[0] == "show":
			self.show()
		elif args[0] == "stop":
			if (len(args) == 3):
				bid = int(args[1])
				count = int(args[2])
				self.setGoal(bid, count)
			elif (len(args) == 2):
				bid = int(args[1])
				self.setGoal(bid)

cb = CountAndBreak()

def newInstance(event):
	print("Counter Breakpoint exit event:", event.inferior.pid)
	cb.clear()

gdb.events.exited.connect(newInstance)

