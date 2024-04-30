"""RIGOL’s 1000Z Series Digital Oscilloscope
"""

from heimdallr.instrument_control.categories.all_ctgs import *

class LakeShoreModel335(PIDTemperatureControllerCtg):
	
	RANGE_OFF = 0
	RANGE_LOW = 1
	RANGE_MID = 2
	RANGE_HIGH = 3
	
	def __init__(self, address:str, log:LogPile):
		super().__init__(address, log)
	
	def set_setpoint(self, temp_K:float, channel:int=1):
		self.inst.write(f"SETP {channel},{temp_K}")
	def get_setpoint(self, channel:int=1):
		return float(self.inst.query(f"SETP? {channel}"))
	
	def get_temp(self, temp_K:float, channel:int=1):
		return float(self.inst.query(f"SETP? {channel}"))
	
	def set_pid(self, P:float, I:float, D:float, channel:int=1):
		P = max(0.1, min(P, 1000))
		I = max(0.1, min(I, 1000))
		D = max(0.1, min(D, 1000))
		
		# Print a warning if any variable was adjusted
		if P != P or I != I or D != D:
			self.log.error(f"Did not apply command. Instrument limits values to 0.1-1000 and this range was violated.")
			return
		self.write(f"PID {channel}")
	
	def get_pid(self, channel:int=1):
		
		pid_str = self.query(f"PID? {channel}")
		print(pid_str)
		
		# Split at commas
		pidstr_list = pid_str.split(",")
		
		# Format into array of numbers
		pid_list = [float(x) for x in pidstr_list]
		
		# Return values as dictionary
		return {"P": pid_list[0], "I": pid_list[1], "D": pid_list[2]}
	
	def set_range(self, range:int, channel:int=1):
		
		range = max(0, min(range, 3))
		if range != range:
			self.log.error(f"Did not apply command. Invalid range parameter supplied. Use range constants built into class.")
			return
		
		self.write(f"RANGE {channel},{range}")
	def get_range(self, channel:int=1):
		return int(self.query(f"RANGE? {channel}"))
	
	def set_enable(self, enable:bool, channel:int=1):
		pass
		#PRobably OUTMODE command, but should play around with this