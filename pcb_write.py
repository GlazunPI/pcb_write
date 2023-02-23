import svgwrite
import math

from svgwrite import mm

track_width = 1
track_to_track_distance = 1
plate_width = 200
plate_height = 200
padding_w = 10
padding_h = 10
w = plate_width-padding_w*2
h = plate_height-padding_h*2
track_count = int(w/(track_width + track_to_track_distance))
copper_thiknes_um = 18
u=220

def drawLine(dwg, start, end, width):
	dwg.add(dwg.line(start=(start[0]*mm, start[1]*mm),
					end=(end[0]*mm, end[1]*mm),
					stroke='black',
					stroke_width=width*mm,
					stroke_linecap='round'))

def calcResistance(lenth, width, thiknes, temp=100):
	#lenth im meters
	#width im mm
	#thiknes in um
	#temp deegres celsius
	#From:
	#http://circuitcalculator.com/wordpress/2006/01/24/trace-resistance-calculator/
	temp_co	= 0.0039 #Om^-1
	resistivity = 0.0172 #Om*mm^2/m
	return resistivity*lenth/(width*thiknes*0.001)*(1 + (temp_co*(temp - 20)))

def calcDistance(x1, y1, x2, y2):
		return  math.sqrt(pow(x1-x2, 2)) + math.sqrt(pow(y1-y2, 2))

def get_lines_type1(w, h, padding_w, padding_h, track_width, track_to_track_distance):
	track_count = int(w/(track_width + track_to_track_distance))
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

def draw_pcb():
	wire_lenth = 0
	dwg = svgwrite.Drawing('pcb.svg', profile='tiny', size=(plate_width*mm, plate_height*mm))
	lines = get_lines_type1(w, h, padding_w, padding_h, track_width, track_to_track_distance)
	wire_lenth = 0
	for line in lines:
		drawLine(dwg, line[0], line[1], track_width)
		wire_lenth = wire_lenth + calcDistance(line[0][0], line[0][1], line[1][0], line[1][1])
	dwg.save()
	return wire_lenth

if __name__ == '__main__':
	wire_lenth = draw_pcb()
	print('Coper thiknes is: ', copper_thiknes_um, 'um')
	print('Track width is: ', track_width, 'mm')
	print('Track to track distamce is: ', track_to_track_distance, 'mm')
	print('Totol lenth is: ', wire_lenth, 'mm')
	r = calcResistance(wire_lenth/1000, track_width, copper_thiknes_um)
	print('Resistance is: ', r, 'Om')
	print('Current is :', u/r, 'Amps')
	print('Power is: ', u*u/r, 'Watt')
