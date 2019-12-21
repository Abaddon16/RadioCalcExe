from math import tan
from math import atan
from math import radians
from math import degrees


class SectorValues:
	def __init__(self):
		self.dist, self.alt = None, None
		self.top, self.tgt, self.bot = None, None, None
		self.O1, self.O2 = None, None
		
	def assign_values(self, dist, alt, top, tgt, bot, O1, O2):
		self.dist, self.alt = dist, alt
		self.top, self.tgt, self.bot = top, tgt, bot
		self.O1, self.O2 = O1, O2
	
	def clear_values(self):
		self.dist, self.alt=None, None
		self.top, self.tgt, self.bot=None, None, None
		self.O1, self.O2=None, None
		
	def dict_values(self):
		return {
			"dist": self.dist, "alt": self.alt,
			"top": self.top, "tgt": self.tgt, "bot": self.bot,
			"O1":  self.O1, "O2": self.O2
			}
	def self_values(self):
		return [self.dist, self.alt, self.top, self.tgt, self.bot, self.O1, self.O2]
		
	def __repr__(self):
		return  "========================================" +\
			    "Distance: " + str(self.dist) + " ft\n" +\
				"Node Alt: " + str(self.alt) + " ft\n" +\
				"Top: " + str(self.top) + " ft\n" +\
				"Tgt Alt: " + str(self.tgt) + " ft\n" +\
				"Bot: " + str(self.bot) + " ft\n" +\
				"O1: " + str(self.O1) + "*\n" +\
				"O2: " + str(self.O2) + "*\n" + \
				"========================================"
	
	def solve(self, static_vals):
		static_vals=set(static_vals)
		# TODO: determine best solve path for different variable combos
		for x in range(3):#random attempts to just... force it to solve for everything without recursion
			if "_dist_" not in static_vals:
				if [self.alt, self.bot, self.O1, self.O2].count(None)==0 or \
						[self.alt, self.top, self.O1, self.O2].count(None)==0 or \
						[self.alt, self.tgt, self.O2].count(None)==0:
					self.find_dist()
			if "_O2_" not in static_vals:
				if [self.alt, self.tgt, self.dist].count(None)==0 or \
						[self.alt, self.top, self.dist, self.O1].count(None)==0 or \
						[self.alt, self.bot, self.dist, self.O1].count(None)==0:
					self.find_O2()
			if "_bot_" not in static_vals:# TODO: update with tgt equations
				if [self.alt, self.dist, self.O1, self.O2].count(None)==0 or \
						[self.top, self.dist, self.O1, self.O2].count(None)==0:
					self.find_bot()
			if "_tgt_" not in static_vals:
				if [self.alt, self.dist, self.O2].count(None)==0 or \
						[self.top, self.dist, self.O1, self.O2].count(None)==0 or \
						[self.bot, self.dist, self.O1, self.O2].count(None)==0:
					self.find_tgt()
			if "_top_" not in static_vals:# TODO: update with tgt equations
				if [self.alt, self.dist, self.O1, self.O2].count(None)==0 or \
						[self.bot, self.dist, self.O1, self.O2].count(None)==0:
					self.find_top()
			if "_alt_" not in static_vals:
				if [self.top, self.dist, self.O1, self.O2].count(None)==0 or \
						[self.bot, self.dist, self.O1, self.O2].count(None)==0 or \
						[self.tgt, self.dist, self.O2].count(None)==0:
					self.find_alt()
		return "Can't Calculate - Check variable combo and try again" if self.self_values().count(None)>0 else None
	
	# solve for needed radio Altitude
	# alt = top-(dist)tan(O1/2)-(dist)tan(O2)  [top, dist, O1, O2]
	#     = bot+(dist)tab(O1/2)-(dist)tan(O2)  [bot, dist, O1, O2]
	#     = tgt-(dist)tan(O2)                  [tgt, dist, O2]
	def find_alt(self):
		try: O1, O2=radians(self.O1), radians(self.O2)
		except TypeError: return "Cannot calculate"
		"""
		Given specific combos of parameters, returns the needed altitude
			[top, dist, O1, O2] or [bot, dist, O1, O2] or [tgt, dist, O2]
		"""
		if O2==0 and self.tgt is not None: self.alt=self.tgt #the antenna isn't angled, so the center of the cone is at the same height as the node
		elif [self.top, self.dist, O1, O2].count(None)==0: self.alt=self.top-self.dist*tan(O2+O1/2)# eq 1
		elif [self.bot, self.dist, O1, O2].count(None)==0: self.alt=self.bot-self.dist*tan(O2-O1/2)# eq 2
		elif [self.tgt, self.dist, O2].count(None)==0: self.alt=self.tgt-self.dist*tan(O2)# eq 3
		else: return "Variable combo not recognized"
		return self.alt
		
	# TODO: Add equation based on "tgt"
	# solve for expected Top Alt
	# top = alt+(dist)*tan(O2+O1/2)                  [alt, dist, O1, O2]
	#     = bot-(dist)*[tan(O2-O1/2)-tan(O2+O1/2)]   [bot, dist, O1, O2]
	def find_top(self):
		try: O1, O2=radians(self.O1), radians(self.O2)
		except TypeError: return "Cannot calculate"
		"""
		Given specific combos of parameters, returns the target altitude
			[alt, dist, O1, O2] or [bot, dist, O1, O2]
		"""
		if [self.alt, self.dist, O1, O2].count(None)==0: self.top=self.alt+self.dist*tan(O2+O1/2)  # eq 1
		elif [self.bot, self.dist, O1, O2].count(None)==0: self.top=self.bot-self.dist*(tan(O2-O1/2)-tan(O2+O1/2))  # eq 2
		else: return "Variable combo not recognized"
		return self.top
	
	# solve for needed Target Alt
	# tgt = alt+(dist)tan(O2)                   [alt, dist, O2]
	#     = top-(dist)*[tan(O2+O1/2)-tan(O2)]   [top, dist, O1, O2]
	#     = bot-(dist)*[tan(O2-O1/2)-tan(O2)]   [bot, dist, O1, O2]
	def find_tgt(self):
		try: O1, O2=radians(self.O1), radians(self.O2)
		except TypeError: return "Cannot calculate"
		"""
		Given specific combos of parameters, returns the target altitude
			[alt, dist, O2] or [top, dist, O1, O2] or [bot, dist, O1, O2]
		"""
		if O2==0 and self.alt is not None: self.tgt=self.alt #the antenna isn't angled, so the center of the cone is at the same height as the node
		elif [self.alt, self.dist, O2].count(None)==0: self.tgt=self.alt+self.dist*tan(O2)# eq 1
		elif [self.top, self.dist, O1, O2].count(None)==0: self.tgt=self.top-self.dist*(tan(O2+O1/2)-tan(O2))# eq 2
		elif [self.bot, self.dist, O1, O2].count(None)==0: self.tgt=self.bot-self.dist*(tan(O2-O1/2)-tan(O2))#eq 3
		else: return "Variable combo not recognized"
		return self.tgt
	
	# TODO: Add equation based on "tgt"
	# solve for expected Bottom Alt
	# bot = alt+(dist)*tan(O2-O1/2)                 [alt, dist, O1, O2]
	#     = top-(dist)*[tan(O2+O1/2)-tan(O2-O1/2)]  [top, dist, O1, O2]
	def find_bot(self):
		try: O1, O2=radians(self.O1), radians(self.O2)
		except TypeError: return "Cannot calculate"
		"""
		Given specific combos of parameters, returns the target altitude
			[alt, dist, O1, O2] or [top, dist, O1, O2]
		"""
		if [self.alt, self.dist, O1, O2].count(None)==0: self.bot=self.alt+self.dist*tan(O2-O1/2)#eq 1
		elif [self.top, self.dist, O1, O2].count(None)==0: self.bot=self.top-self.dist*(tan(O2+O1/2)-tan(O2-O1/2))#eq 2
		else: return "Variable combo not recognized"
		return self.bot
	
	# solve for needed Omega 2
	# O2 = tan^(-1)((tgt-alt)/dist)            [alt, tgt, dist]
	#    = tan^(-1)((top-alt)/dist)-O1/2       [alt, top, dist, O1]
	#    = tan^(-1)((bot-alt)/dist)+O1/2       [alt, bot, dist, O1]
	def find_O2(self):
		O1=radians(self.O1)
		"""
		Given specific combos of parameters, returns the target altitude
			[alt, tgt, dist] or [alt, top, dist, O1] or [alt, bot, dist, O1]
		"""
		if (self.alt is not None and self.tgt is not None) and self.alt==self.tgt: self.O2=0#if the tgt and the alt are the same, the antenna isn't angled
		if [self.tgt, self.alt, self.dist].count(None)==0: self.O2=atan((self.tgt-self.alt)/self.dist)#eq 1
		elif [self.top, self.alt, self.dist, O1].count(None)==0: self.O2=atan((self.top-self.alt)/self.dist)-O1/2#eq 2
		elif [self.bot, self.alt, self.dist, O1].count(None)==0: self.O2=atan((self.bot-self.alt)/self.dist)+O1/2#eq 3
		else: return "Variable combo not recognized"
		return degrees(self.O2)
	
	# solve for needed Distance
	# dist = (bot-alt)/tan(O2-O1/2)   [alt, bot, O1, O2]
	#      = (top-alt)/tan(O2-O1/2)   [alt, top, O1, O2]
	#      = (tgt-alt)/tan(O2)        [alt, tgt, O2]
	def find_dist(self):
		try: O1, O2=radians(self.O1), radians(self.O2)
		except TypeError: return "Cannot calculate"
		"""
		Given specific combos of parameters, returns the needed distance
			[alt, bot, O1, O2] or [alt, top, O1, O2] or [alt, tgt, O2]
		"""
		if [self.alt, self.bot, O1, O2].count(None)==0: self.dist=(self.bot-self.alt)/tan(O2-O1/2)
		elif [self.alt, self.top, O1, O2].count(None)==0: self.dist=(self.top-self.alt)/tan(O2+O1/2)
		elif [self.alt, self.tgt, O2].count(None)==0:
			if O2==0: self.dist=0 #tgt = alt :: distance needed to get to that altitude is... 0 :'(
			else: self.dist=(self.tgt-self.alt)/tan(O2)
		else: return "Variable combo not recognized"
		return self.dist
