
import matplotlib.pyplot as plt
import time
import random
import cv2
import math

def image_to_feature_vector(image, size=(16, 16)):
    # resize the image to a fixed size, then flatten the image into
    # a list of raw pixel intensities
    return cv2.resize(image, size).flatten()

k=256

#Nuestra clase nodo
class Node():
    """docstring for Node"""
    def __init__(self, point):
        self.point = point
        self.axis = None
        self.left = None
        self.right = None
        self.tipo = None

class Cola():
	"""docstring for Cola"""
	def __init__(self, cant):
		self.n = cant
		self.lis=[]
	def agregar(self, distancia,x):
		for i in range(len(self.lis)):
			if(self.lis[i][1]==x):
				return
		if(len(self.lis)==self.n):
			if(self.lis[self.n-1][0]>distancia):
				self.lis[self.n-1]=[distancia,x]
				self.lis.sort(key=lambda tup: tup[0])
		else:
			self.lis.append([distancia,x])
			self.lis.sort(key=lambda tup: tup[0])
	def top(self):
		return self.lis[len(self.lis)-1][0]
	def llena(self):
		if(len(self.lis)!=self.n):
			return False
		return True

#Aqui construimos el kd tree
def build_kdtree(points, depth=0):
	if not points:
		return None
	#Para saber si dividir por el eje x o y
	axis = depth % k

	points.sort(key=lambda tup: tup.point[axis])

	median = len(points)//2

	node = points[median]
	node.axis=axis

	node.left=build_kdtree(points[:median],depth+1)
	node.right=build_kdtree(points[median+1:],depth+1)

	return node

def distanceSquared(a, b):
	distance = 0
	for i in range(k):
		distance = distance + pow((a[i]-b[i]),2)
	return math.sqrt(distance)

def closest_point(node, point, depth , cola):
	if(node == None):
		return
	axis = depth % k
	next_branch = None
	opposite_branch = None
	cola.agregar(distanceSquared(point, node.point),node)
	if(point[axis] < node.point[axis]):
		next_branch = node.left
		opposite_branch = node.right
	else:
		next_branch = node.right
		opposite_branch = node.left
	closest_point(next_branch, point, depth+1, cola)
	if(not(cola.llena()) or (cola.top() > abs(point[axis]-node.point[axis]))):
		closest_point(opposite_branch, point, depth+1, cola)

def nearest(root, point, count):
	cola = Cola(count)
	closest_point(root, point, 0, cola)
	return cola.lis

def main():
    #Cremos una lista con valores aleatorios para hacer el kdtree
    points=[]
    con=0
    t=0
    for i in range(1,36):
        name="perro"+str(i)+".png"
        image = cv2.imread(name)
        pixels = image_to_feature_vector(image)
        l=[]
        con=0
        t=0
        for i in range(len(pixels)):
            con=con+pixels[i]
            if(t==2):
                l.append(con/3)
                t=0
                con=0
            else:
                t=t+1
        	
        
        node = Node(l)
        node.tipo="perro"
        points.append(node)
    
    for i in range(1,36):
        name="loro"+str(i)+".png"
        image = cv2.imread(name)
        pixels = image_to_feature_vector(image)
        l=[]
        con=0
        t=0
        for i in range(len(pixels)):
            con=con+pixels[i]
            if(t==2):
                l.append(con/3)
                t=0
                con=0
            else:
                t=t+1

        node = Node(l)
        node.tipo="loro"
        points.append(node)

    root=build_kdtree(points)
    #image = cv2.imread("loro17.png")
    image = cv2.imread("prueba.png")
    pixels = image_to_feature_vector(image)
    resul = nearest(root, pixels, 10)
    cp=0
    cl=0
    for i in resul:
    	if(i[1].tipo=="perro"):
    		cp=cp+1
    	else:
    		cl=cl+1
    if(cp>cl):
    	print("Es un perro")
    else:
    	print("Es un loro")

    print(cp,cl)
main()
