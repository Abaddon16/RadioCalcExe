# TODO: create checkboxes to determine which to solve for vs (current state of) if values exist or not




import PySimpleGUI as sg
from SectorValues import SectorValues

def conToNum(s):
	if s is None: return None
	try: return int(s)
	except ValueError: pass
	try: return float(s)
	except ValueError: return None
	
def conUnit(win, boxName, oldValue, newUnit, updateWindow: bool):
	if dist_prev_sel[boxName]==newUnit: return conToNum(oldValue)
	newValue=round(conToNum(oldValue)/conversion[dist_prev_sel[boxName]][newUnit], 3)
	if updateWindow: win.Element(boxName).Update(newValue)
	dist_prev_sel[boxName]=newUnit
	return newValue

def getBoxName(s: str):
	return '_'+s.split('_')[-1]+'_'
	
radioAttrs=["_dist_", "_alt_", "_top_", "_tgt_", "_bot_", "_O1_", "_O2_"]
distances=['feet', 'miles', 'nautical miles', 'meters', 'kilometers']# any update here will need to update the `conversion` dict and the distance_prev_selection dict
conversion={#divide by these values; this is why miles -> feet has 1/5280: 2/(1/5280)=2*5280; newValue=oldValue/conversion[oldUnit][newUnit]
			'feet': {'miles': 5280, 'nautical miles': 6076.115, 'meters': 3.2808, 'kilometers': 3280.8},
			'miles': {'feet': 1/5280, 'nautical miles': 6076.115/5280, 'meters': 0.0006213712, 'kilometers': 0.62137},
			'nautical miles': {'feet': 1/6076.115, 'miles': 5280/6076.115, 'meters': 1/1852, 'kilometers': 1/1.852},
			'meters': {'feet': 1/3.2808, 'miles': 1/0.0006213712, 'nautical miles': 1852, 'kilometers': 1000},
			'kilometers': {'feet': 1/3280.8, 'miles': 1/.62137, 'nautical miles': 1.852, 'meters': 1/1000}
			}
dist_prev_sel={'_dist_': 'feet', '_alt_': 'feet', '_top_': 'feet', '_tgt_': 'feet', '_bot_': 'feet'}


def createWindow():
	sg.ChangeLookAndFeel('Dark')
	intro_layout=\
			[
				[sg.Multiline(size=(40, 15), disabled=True,
							  default_text="This is a calculator with many assumptions:\n"+\
				                            "1) Line of Sight is assumed\n"+\
				                            "2) Distances are not modulated (if it's too far, it won't tell you)\n\n"+\
				                            "Hover over the value name for a tooltip to see what data is needed to solve for that particular value.\n\n"+\
				                            "Check the box next to values you want to keep static.")]
			]
	calc_layout=\
			[
				[sg.Checkbox('', key="check_dist", default=False),
				 sg.Text('Distance', tooltip="Ground Distance from Node to Target\n\n"+"[alt, bot, O1, O2]\n[alt, top, O1, O2]\n[alt, tgt, O2], O2!=0",
				         size=(10, 1)),
				 sg.Input(key='_dist_', size=(10, 1), focus=True),
				 sg.Combo(distances, enable_events=True, key="combo_dist", readonly=True)
				 ],
				[sg.Checkbox('', key="check_alt", default=False),
				 sg.Text('Node Alt', tooltip="Alt of the transmitting Node\n\n"+"[top, dist, O1, O2]\n[bot, dist, O1, O2]\n[tgt, dist, O2]",
				         size=(10, 1)),
				 sg.Input(key='_alt_', size=(10, 1)),
				 sg.Combo(distances, enable_events=True, key="combo_alt",  readonly=True)
				 ],
				[sg.Checkbox('', key="check_top", default=False),
				 sg.Text('Top Alt', tooltip="Alt of the top of the transmit cone\n\n"+"[alt, dist, O1, O2]\n[bot, dist, O1, O2]",#TODO: update w tgt equation
				         size=(10, 1)),
				 sg.Input(key='_top_', size=(10, 1)),
				 sg.Combo(distances, enable_events=True, key="combo_top",  readonly=True)
				 ],
				[sg.Checkbox('', key="check_tgt", default=False),
				 sg.Text('Target Alt', tooltip="Alt of middle of the transmit cone\n\n"+"[alt, dist, O2]\n[top, dist, O1, O2]\n[bot, dist, O1, O2]",
				         size=(10, 1)),
				 sg.Input(key='_tgt_', size=(10, 1)),
				 sg.Combo(distances, enable_events=True, key="combo_tgt",  readonly=True)
				 ],
				[sg.Checkbox('', key="check_bot", default=False),
				 sg.Text('Bottom Alt', tooltip="Alt of the bottom of the transmit cone\n\n"+"[alt, dist, O1, O2]\n[top, dist, O1, O2]",#TODO update w tgt equation
				         size=(10, 1)),
				 sg.Input(key='_bot_', size=(10, 1)),
				 sg.Combo(distances, enable_events=True, key="combo_bot",  readonly=True)
				 ],
				[sg.Checkbox('', key="check_O1", default=True),
				 sg.Text('Theta 1 (O1)', tooltip="Angle(deg) of the vertical beam width of the transmit cone",
				         size=(10, 1)),
				 sg.Input(key='_O1_', size=(10, 1), default_text=8),
				 sg.Text('degrees')
				 ],
				[sg.Checkbox('', key="check_O2", default=False),
				 sg.Text('Theta 2 (O2)', tooltip="Angle(deg) of the rotation of the transmit cone\n\n"+"[alt, tgt, dist]\n[alt, top, dist, O1]\n[alt, bot, dist, O1]",
				         size=(10, 1)),
				 sg.Input(key='_O2_', size=(10, 1)),
				 sg.Text('degrees')
				 ]
			]+\
			[[sg.Button('Calculate'), sg.Button('Clear'), sg.Button('Exit')]]
	
	layout=[[sg.TabGroup([[sg.Tab('Intro', intro_layout), sg.Tab('Calculations', calc_layout)]])]]
	return sg.Window('Radio Params Calculator', layout)

window=createWindow()
while True: # Event Loop
	event, values = window.Read()
	#print(event, values)
	if event is None or event == 'Exit': break
	if event == 'Calculate':
		sector=SectorValues()
		old_units, conv_values={}, {}
		static_vals=[]
		for x in values:
			if type(x) is str and "combo" in x:
				box=getBoxName(x)
				old_units[box]=values[x]
				conv_values[box]=conUnit(window, box, values[box], "feet", False)
			if type(x) is str and "check" in x and values[x]==True:
				box=getBoxName(x)
				static_vals.append(box)
		sector.assign_values(conToNum(conv_values['_dist_']), conToNum(conv_values['_alt_']), conToNum(conv_values['_top_']), conToNum(conv_values['_tgt_']),
		                     conToNum(conv_values['_bot_']), conToNum(values['_O1_']), conToNum(values['_O2_']))
		ret=sector.solve(static_vals)
		if ret is not None: sg.PopupError(ret, title="Calculation Error")
		for val in radioAttrs:
			value=sector.dict_values()[val[1:-1]] #val[1:-1] gets rid of the '_'s
			if value is not None:
				if val in old_units: value=conUnit(window, val, value, old_units[val], False)
				window.Element(val).Update(round(value, 3))
		sector.clear_values()
	elif "combo" in event:
		box=getBoxName(event)
		data=values[box]
		if conToNum(data) is None: window.Element(box).Update('')
		else: conUnit(window, box, data, values[event], True)
	elif event=="Clear":
		for field in radioAttrs: window.Element(field).Update('')
		window.Element('_O1_').Update(8)
window.Close()