import svgwrite
import math
from svgwrite import mm

class BoardConfig:
	def __init__(self,
				track_width = 1,
				track_to_track_distance = 1,
				plate_width = 200,
				plate_height = 200,
				padding_w = 10,
				padding_h = 10,
				copper_thiknes_um = 18,
				u=220,
				temperature=100):
		self.track_width = track_width
		self.track_to_track_distance = track_to_track_distance
		self.plate_width = plate_width
		self.plate_height = plate_height
		self.padding_w = padding_w
		self.padding_h = padding_h
		self.w = plate_width-padding_w*2
		self.h = plate_height-padding_h*2
		self.copper_thiknes_um = copper_thiknes_um
		self.u = u
		self.temperature = temperature

def draw_line(dwg, start, end, width):
	dwg.add(dwg.line(start=(start[0]*mm, start[1]*mm),
					end=(end[0]*mm, end[1]*mm),
					stroke='black',
					stroke_width=width*mm,
					stroke_linecap='round'))

def calc_resistance(lenth, width, thiknes, temp):
	#lenth im meters
	#width im mm
	#thiknes in um
	#temp deegres celsius
	#From:
	#http://circuitcalculator.com/wordpress/2006/01/24/trace-resistance-calculator/
	temp_co	= 0.0039 #Om^-1
	resistivity = 0.0172 #Om*mm^2/m
	return resistivity*lenth/(width*thiknes*0.001)*(1 + (temp_co*(temp - 20)))

def calc_distance(x1, y1, x2, y2):
		return  math.sqrt(pow(x1-x2, 2)) + math.sqrt(pow(y1-y2, 2))

def calc_track_count(width, track_width, track_to_track_distance):
	return int(width/(track_width + track_to_track_distance))

def get_lines_type1(w, h, padding_w, padding_h, track_width, track_to_track_distance):
	track_count = calc_track_count(w, track_width, track_to_track_distance)
	lines = []
	for track in range(track_count):
		x1 = (track*(track_width+track_to_track_distance)+padding_w)
		y1 = padding_h
		x2 = (track*(track_width+track_to_track_distance)+padding_w)
		y2 = (padding_h + h)
		start_point = (x1, y1)
		end_point = (x2, y2)
		line = [start_point, end_point]
		lines.append(line)
		x2 = (track*(track_width+track_to_track_distance)+track_width + track_to_track_distance + padding_w)
		if (track % 2 == 0):
			start_point = (x1, y1)
			end_point = (x2, y1)
		else:
			start_point = (x1, y2)
			end_point = (x2, y2)
		if track < track_count - 1:
			line = [start_point, end_point]
			lines.append(line)
	return lines

def draw_pcb(config, file_name, draw_method):
	wire_lenth = 0
	dwg = svgwrite.Drawing(file_name, profile='tiny', size=(config.plate_width*mm, config.plate_height*mm))
	lines = draw_method(config.w,
						 config.h,
						 config.padding_w,
						 config.padding_h,
						 config.track_width,
						 config.track_to_track_distance)
	wire_lenth = 0
	for line in lines:
		draw_line(dwg, line[0], line[1], config.track_width)
		wire_lenth = wire_lenth + calc_distance(line[0][0], line[0][1], line[1][0], line[1][1])
	dwg.save()
	return wire_lenth

def print_info(config, wire_lenth):
	print('Coper thiknes is: ', config.copper_thiknes_um, 'um')
	print('Track width is: ', config.track_width, 'mm')
	print('Track to track distamce is: ', config.track_to_track_distance, 'mm')
	print('Totol lenth is: ', wire_lenth, 'mm')
	r = calc_resistance(wire_lenth/1000, config.track_width, config.copper_thiknes_um, config.temperature)
	print('Resistance is: ', r, 'Om at ', config.temperature, ' degrees of Celsius')
	print('Current is :', config.u/r, 'Amps')
	print('Power is: ', config.u*config.u/r, 'Watt')
	print('')

if __name__ == '__main__':
	config = BoardConfig()
	wire_lenth = draw_pcb(config, 'pcb.svg', get_lines_type1)
	print_info(config, wire_lenth)	
	
