# Author: Charles Leifer, Omar Sandoval
##
## This module turns every pixel in the given image,
##   (the users wallpaper in this case),
##   into a 3-dimensional space of RGB. It groups those
##   points into "k" clusters and the mean of those
##   clusters is found. From that we find the most 
##   dominant colors in the image. PIL is used to resize 
##   the image and to extract the colors.
##
## tl;dr Create a color scheme for URxvt from the 
##   dominant colors in your wallpaper!

from collections import namedtuple
from math import sqrt
import random
try:
	import Image
except ImportError:
	from PIL import Image

# Create a namedtuple "Point" with the following values.
Point = namedtuple('Point', ('coords', 'n', 'ct'))

# Create a namedtuple "Cluster" with the following values.
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

def getPoints(img):
	points = []
	
	# Get image size and set to variables width and height.
	width, height = img.size
	for count, color in img.getcolors(width * height):
		points.append(Point(color, 3, count))
	return points

# This part confuses me. Not sure what is going here.
rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))


# Returns color codes for a filename
def colorz(filename, n = 3):
	img = Image.open(filename)
	
	# Turn provided image into a thumbnail 200px by 200px
	img.thumbnail((200, 200))
	# Get new size the the image thumbnail
	width, height = img.size
	
	# Calls getPoints for the new thumbnail
	points = getPoints(img)
	
	# Compute K-Means for those points
	clusters = kmeans(points, n, 1)
	
	# Plot red green and blue points
	rgbs = [map(int, c.center.coords) for c in clusters]
	return map(rtoh,rgbs)
	
def euclidean(p1, p2):
	return sqrt(sum([(p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)]))

# Calculate the center of each cluster
def calculateCenter(points, n):
	vals = [0.0 for i in range(n)]
	plen = 0
	
	# Iterate over p.ct
	for p in points:
		plen += p.ct
		for i in range(n):
			vals[i] += (p.coords[i] * p.ct)
	return Point([(v / plen) for v in vals], n, 1)

# K-Means clustering for each point in 3D RGB
def kmeans(points, k, min_diff):
	clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]
	
	while 1:
		plists = [[] for i in range(k)]
		
		for p in points:
			smallestDistance = float('Inf')
			for i in range(k):
				distance = euclidean(p, clusters[i].center)
				if distance < smallestDistance:
					smallestDistance = distance
					idx = i
			plists[idx].append(p)
		
		diff = 0
		for i in range(k):
			old = clusters[i]
			center = calculateCenter(plists[i], old.n)
			new = Cluster(plists[i], center, old.n)
			clusters[i] = new
			diff = max(diff, euclidean(old.center, new.center))
			
		if diff < min_diff:
			break
		
	return clusters
	
