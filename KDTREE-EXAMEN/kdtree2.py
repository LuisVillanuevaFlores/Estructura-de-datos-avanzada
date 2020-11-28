import networkx as nx
import matplotlib.pyplot as plt
import time
import pygame,sys
from pygame.locals import *
import random

#Creamos esta funcion para no confundirnos
#ya que pygame tiene las coordenadas del eje Y invertidas
def camb(y):
	return 800-y

def camb2(x):
	return x+20

#Creamos nuestra ventana
pygame.init()
ventana = pygame.display.set_mode((1000,900))
Color2=pygame.Color(255,255,255)
pygame.draw.line(ventana,Color2,(0+20,camb(0)),(0+20,camb(800)),10)
pygame.draw.line(ventana,Color2,(0+20,camb(0)),(900+20,camb(0)),10)
pygame.display.set_caption("Kd-Tree")

#funte para escribir la coordenada de los puntos
fuente = pygame.font.Font(None, 30)

#En este array guardaremos el punto inicial y final
#de donde deberia ir la recta que generan los puntos
#el orden para las 3 listas es preorden
v=[]
#Aqui guardamos los colores que tocan a cada recta
co=[]
#Aqui guardamos las coordenas de los puntos para 
#dibujar las coordenadas de los puntos
pp=[]
#Creación de nuestro grafo dirigido
G = nx.DiGraph()

k=2

#Nuestra clase nodo
class Node():
	"""docstring for Node"""
	def __init__(self, point, axis):
		self.point = point
		self.axis = axis
		self.left = None
		self.right = None
		#Limite mayor en el eje x
		self.Mx = None
		#Limite menor en el eje x
		self.mx = None
		#Limite mayor en el eje y
		self.My = None
		#Limite menor en el eje y
		self.my = None
#Ordenar por y
def orde(tupla):
  return (tupla[1], -tupla[0])

#Ordenar por x
def ord2(tupla):
  return (tupla[0], -tupla[1])

#Aqui construimos el kd tree
def build_kdtree(points, depth=0):
	if not points:
		return None
	#Para saber si dividir por el eje x o y
	axis = depth % k
	if(axis==0):
		points=sorted(points, key=ord2)
	else:
		points=sorted(points, key=orde)

	median = len(points)//2

	node = Node(points[median], axis)

	node.left=build_kdtree(points[:median],depth+1)
	node.right=build_kdtree(points[median+1:],depth+1)

	return node

#Aqui recorremos el arbol en preorden para definir los limites de cada punto
def limi(root):
	if(root==None):
		return

	if(root.axis==0):
		if(root.left!=None):
			root.left.mx = root.mx
			root.left.Mx = root.point[0]
			root.left.my = root.my
			root.left.My = root.My
		if(root.right!=None):
			root.right.mx = root.point[0]
			root.right.Mx = root.Mx
			root.right.my = root.my
			root.right.My = root.My
	else:
		if(root.left!=None):
			root.left.mx = root.mx
			root.left.Mx = root.Mx
			root.left.my = root.my
			root.left.My = root.point[1]
		if(root.right!=None):
			root.right.mx = root.mx
			root.right.Mx = root.Mx
			root.right.my = root.point[1]
			root.right.My = root.My

	limi(root.left)
	limi(root.right)

#Aqui tambien recorremos el arbol para sacar los limites y saber
#de donde a donde dibujar la linea divisora
def agreg(root):
	if(root==None):
		return
	if(root.axis==0):
		if(root.left!=None):
			x=root.point[0]
			y=root.left.point[1]
			pi=[[x,y],[root.mx,y]]
			v.append(pi)
			co.append(1)
			aa=root.left.point
			pp.append(aa)
		if(root.right!=None):
			x=root.point[0]
			y=root.right.point[1]
			pi=[[x,y],[root.Mx,y]]
			v.append(pi)
			co.append(1)
			aa=root.right.point
			pp.append(aa)
	else:
		if(root.left!=None):
			y=root.point[1]
			x=root.left.point[0]
			pi=[[x,y],[x,root.my]]
			v.append(pi)
			co.append(0)
			aa=root.left.point
			pp.append(aa)
		if(root.right!=None):
			y=root.point[1]
			x=root.right.point[0]
			pi=[[x,y],[x,root.My]]
			v.append(pi)
			co.append(0)
			aa=root.right.point
			pp.append(aa)

	agreg(root.left)
	agreg(root.right)

def grafi(node):
    if(node==None):
        return
    if(node.left!=None):
        G.add_node(node.point) #creamos un nodo y lo agregamos a nuesro grafo
        G.add_node(node.left.point) #creamos el nodo con el hijo izquierdo
        G.add_edge(node.point,node.left.point) # creamos la arista entre ambos
		
    if(node.right!=None):
        G.add_node(node.point) #creamos un nodo y lo agregamos a nuesro grafo
        G.add_node(node.right.point) #creamos el nodo con el hijo derecho
        G.add_edge(node.point,node.right.point)# creamos la arista entre ambos
        
	#llamamos recursivamente a sus hijos izquierdo y derecho para realizar la misma accion 	
    grafi(node.left)
    grafi(node.right)

''' Funcion para dibujar un arbol'''
def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
    if pos is None:
        pos = {root:(xcenter,vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)  
    if len(children)!=0:
        dx = width/len(children) 
        nextx = xcenter - width/2 - dx/2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
            vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos, 
            parent = root)
    return pos

def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')
    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))
        else:
            root = random.choice(list(G.nodes))
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

def main():
	#Cremos una lista con valores aleatorios para hacer el kdtree
	points=[]
	for i in range (10):
		x=random.randint(0, 18)
		y=random.randint(0, 16)
		points.append((x,y))
	#points=[(7,2), (5,4), (9,6), (4,7), (8,1), (2,3)]
	#Construimosl arbol
	root=build_kdtree(points)
	#seteamos los limites iniciales despues de conocer la raiz
	root.mx=0
	root.Mx=18
	root.my=0
	root.My=16
	#sacamos los limites
	limi(root)
	#Le mandamos a v los valores para construir la primera linea
	pi=[[root.point[0],0],[root.point[0],16]]
	v.append(pi)
	#Le asignamos a esta el color azul
	co.append(0)
	aa=root.point
	pp.append(aa)
	agreg(root)
	#i sera nuestro iterador de los puntos
	i=0
	grafi(root)
	pos = hierarchy_pos(G,root.point)
	nx.draw(G, pos=pos, node_size=2000,with_labels=True)
	plt.savefig('arbol.png') #guardamos la imagen del arbol
	while True:
		#Hacemos un loop para que la ventana funcione
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			#Colocamos este evento para hacer que avance con la tecla Left
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					#Cuando ya se hayan recorrido todos los puntos, reiniciamos la pantalla
					#Para volverla a mostrar
					if(i==len(v)):
						ventana.fill((0,0,0))
						pygame.draw.line(ventana,Color2,(20,camb(0)),(20,camb(800)),10)
						pygame.draw.line(ventana,Color2,(20,camb(0)),(900+20,camb(0)),10)
						i=0
					else:
						#Le damos el color que corresponde a nuestra variable Color
						if(co[i]==0):
							Color=pygame.Color(0,0,255)
						else:
							Color=pygame.Color(255,0,0)
						#vamos imprimiendo los puntos en consola
						print(pp[i])
						#Transformamos el punto en string para mandarlo a pantalla
						text=" ".join(str(x) for x in pp[i])
						mensaje=fuente.render(text,1,(0,255,0))
						#Aqui dibujamos nuestra linea, lo multiplicamos por 50 para hacer una escala
						#Ya que nuestra pantalla es 900*800
						pygame.draw.line(ventana,Color,(v[i][0][0]*50+20,camb(v[i][0][1]*50)),(v[i][1][0]*50+20,camb(v[i][1][1]*50)),10)
						ventana.blit(mensaje,(pp[i][0]*50-15+20,camb(pp[i][1]*50)))
						#Aumentamos en 1 nuestor iterador
						i=i+1
		pygame.display.update()	

	print(root.point)
main()
