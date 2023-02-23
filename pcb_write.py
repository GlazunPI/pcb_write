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
	dwg.add(dwg.line(start=start,
					end=end,
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

def draw_pcb():
	wire_lenth = 0
	dwg = svgwrite.Drawing('pcb.svg', profile='tiny', size=(plate_width*mm, plate_height*mm))
	for track in range(track_count):
		x1 = (track*(track_width+track_to_track_distance)+padding_w)
		y1 = padding_h
		x2 = (track*(track_width+track_to_track_distance)+padding_w)
		y2 = (padding_h + h)
		start_point = (x1*mm, y1*mm)
		end_point = (x2*mm, y2*mm)
		drawLine(dwg, start=start_point, end=end_point, width=track_width)
		distance = math.sqrt(pow(x1-x2, 2)) + math.sqrt(pow(y1-y2, 2))
		wire_lenth = wire_lenth +  distance  
		x2 = (track*(track_width+track_to_track_distance)+track_width+track_to_track_distance+padding_w)
		if (track % 2 == 0):
			start_point = (x1*mm, y1*mm)
			end_point = (x2*mm, y1*mm)
		else:

			start_point = (x1*mm, y2*mm)
			end_point = (x2*mm, y2*mm)
		if track < track_count - 1:
			drawLine(dwg, start=start_point, end=end_point, width=track_width)
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
