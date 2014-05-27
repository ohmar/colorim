# Author: haywire, Omar Sandoval
##
## This program gets the colors provided by the colorz.py
##   module and turns them into hex codes that can be read by
##   programs like urxvt (what we'll be using in this example),
##   herbstluftwm, etc.
## Two files are created by this program. ~/.colors
##   and ~/.Xresources.
## Remember to change USER to your GNU/Linux username. Or the
##   path to your home folder.

# Import required modules, sys (for file paths)
import sys
import colorsys
import os

# Import colorz module to get dominant colors.
from colorz import colorz
DIR = os.getcwd()
wallpaper = DIR+'/.wallpaper'
colors = DIR+'/.colors'
xresources = DIR+'/.Xresources'

cols = ''
xres = """
URxvt.perl-ext-common: default,keyboard-select,url-select,clipboard
URxvt.modifier: super

! Original Colors
! urxvt*color8:    #4DA869
! urxvt*color9:    #EF2929
! urxvt*color10:    #BDA2BF
! urxvt*color11:    #FFF391
! urxvt*color12:    #7587A6
! urxvt*color13:    #F0C47B
! urxvt*color14:    #FF4040
! urxvt*color15:    #EEEEEC
! urxvt*color0:    #2E3436
! !urxvt*color0:    #000000
! urxvt*color1:    #DD1144
! urxvt*color2:    #9B859D
! urxvt*color3:    #F9EE98
! urxvt*color4:    #424D5E
! urxvt*color5:    #CDA869
! urxvt*color6:    #E94444
! urxvt*color7:    #C2C2C2

! Keyboard options. These can depend on you.
! Keyboard select
URxvt.keysym.M-Escape: perl:keyboard-select:activate
URxvt.keysym.M-s: perl:keyboard-select:search

! URL select
URxvt.keysym.M-u: perl:url-select:select_next
URxvt.url-select.autocopy: true
URvxt.url-select.button: 1
URvxt.url-select.launcher: mimeo
URxvt.url-select.underline: true

! Clipboard
URxvt.keysym.M-c:   perl:clipboard:copy
URxvt.keysym.M-v:   perl:clipboard:paste
URxvt.keysym.M-C-v: perl:clipboard:paste_escaped


URxvt.foreground: #ffffff
URxvt.scrollBar: false
URxvt.depth: 32
URxvt.background: [85]#0E0E0E

! Colorz

"""
# Creates RGB colors
def normalize(hexv, minv=128, maxv=256):
	hexv = hexv[1:]
	r, g, b = (
		int(hexv[0:2], 16) / 256.0,
		int(hexv[2:4], 16) / 256.0,
		int(hexv[4:6], 16) / 256.0,
	)
	
	# Convert colors from RGB to HSV for Hue, Saturation, and Value
	h, s, v = colorsys.rgb_to_hsv(r, g, b)
	minv = minv / 256.0
	maxv = maxv / 256.0
	if v < minv:
		v = minv
	if v > maxv:
		v = maxv
	
	# Convert colors from HSV to RGB for Red, Green and Blue
	r, g, b = colorsys.hsv_to_rgb(h, s, v)
	return '#{:02x}{:02x}{:02x}'.format(int(r * 256), int(g * 256), int(b * 256))
	
# If module is running as a program then
if __name__ == '__main__':
	if len(sys.argv) == 1:
		n = 16
	else:
		n = int(sys.argv[1])
             
	i = 0
	# Open colors.html and write your image as a thumbnail 200x200.
	with open('colors.html', 'w') as f:
		f.write("""<img src="file://{}" height=200/>""".format(wallpaper))
		for c in colorz(wallpaper, n=n):
			if i == 0:
				c = normalize(c, minv=0, maxv=32)
			elif i == 8:
				c = normalize(c, minv=128, maxv=192)
			elif i < 8:
				c = normalize(c, minv=160, maxv=224)
			else:
				c = normalize(c, minv=200, maxv=256)
				
			# Write the dominant colors in the image of height 50 pixels
			#   and include their respective hex code.
			f.write("""
				<div style="background-color: {0}; width: 100%; height: 50px">{1}: {0}</div>
				""".format(c, i)
			)
			xres += """urxvt*color{}: {}\n""".format(i, c)
			cols += """export COLOR{}="{}"\n""".format(i, c)
			i += 1
	# Write the ~/.Xresources file			
	with open(xresources, 'w') as f:
		f.write(xres)
	# Write the ~/.colors file
	with open(colors, 'w') as f:
		f.write(cols)
