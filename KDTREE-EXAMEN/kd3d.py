import networkx as nx
import matplotlib.pyplot as plt
import time
from vtk import *
import random

#En este array guardaremos el punto inicial y final
#de donde deberia ir la recta que generan los puntos
#el orden para las 3 listas es preorden
v=[]
#Aqui guardamos los colores que tocan a cada recta
co=[]
#Aqui guardamos las coordenas de los puntos para 
#dibujar las coordenadas de los puntos
pp=[]

G = nx.DiGraph()

k=3

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
		#Limite mayor en el eje z
		self.Mz = None
		#Limite menor en el eje z
		self.mz = None

class Punto():
	"""docstring for Punto"""
	def __init__(self, l, axis):
		self.l=l
		if(axis==0):
			self.color=[0,0,255]
		elif(axis==1):
			self.color=[255,0,0]
		else:
			self.color=[0,255,0]
		
		self.punt = vtkSphereSource()
		self.punt.SetRadius(1)
		self.punt.SetCenter(l[0],l[1],l[2])

		self.puntMapper = vtkPolyDataMapper()
		self.puntMapper.SetInputConnection(self.punt.GetOutputPort())

		self.puntActor = vtkActor()
		#self.puntActor.GetProperty().SetColor(self.color)
		self.puntActor.SetMapper(self.puntMapper)
		

class plane():
	def __init__(self, root):
		self.cube = vtkCubeSource()
		if(root.axis==1):
			self.color=[255,0,0]
			self.cube.SetYLength(0.5)
			self.cube.SetXLength(root.Mx-root.mx)
			self.cube.SetZLength(root.Mz-root.mz)
			self.cube.SetCenter(float((root.Mx+root.mx)/2),root.point[1],float((root.Mz+root.mz)/2))
		elif(root.axis==2):
			self.color=[0,255,0]
			self.cube.SetYLength(root.My-root.my)
			self.cube.SetXLength(root.Mx-root.mx)
			self.cube.SetZLength(0.5)
			self.cube.SetCenter(float((root.Mx+root.mx)/2),float((root.My+root.my)/2),root.point[2])
		else:
			self.color=[0,0,255]
			self.cube.SetYLength(root.My-root.my)
			self.cube.SetXLength(0.5)
			self.cube.SetZLength(root.Mz-root.mz)
			self.cube.SetCenter(root.point[0],float((root.My+root.my)/2),float((root.Mz+root.mz)/2))
		self.cubeMapper = vtkPolyDataMapper()
		self.cubeMapper.SetInputConnection(self.cube.GetOutputPort())
		self.cubeMapper.SetResolveCoincidentTopologyToShiftZBuffer()

		self.cubeActor = vtkActor()
		self.cubeActor.SetMapper(self.cubeMapper)
		self.cubeActor.GetProperty().SetColor(self.color)
		self.cubeActor.GetProperty().SetOpacity(0.5)

#Ordenar por y
def orde(tupla):
  return (tupla[1])

#Ordenar por x
def ord2(tupla):
  return (tupla[0])

#Ordenar por z
def ord3(tupla):
  return (tupla[2])


#Aqui construimos el kd tree
def build_kdtree(points, depth=0):
	if not points:
		return None
	#Para saber si dividir por el eje x, y o z
	axis = depth % k
	if(axis==0):
		points=sorted(points, key=ord2)
	elif(axis==1):
		points=sorted(points, key=orde)
	else:
		points=sorted(points, key=ord3)

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
			root.left.mz = root.mz
			root.left.Mz = root.Mz
		if(root.right!=None):
			root.right.mx = root.point[0]
			root.right.Mx = root.Mx
			root.right.my = root.my
			root.right.My = root.My
			root.right.mz = root.mz
			root.right.Mz = root.Mz
	elif(root.axis==1):
		if(root.left!=None):
			root.left.mx = root.mx
			root.left.Mx = root.Mx
			root.left.my = root.my
			root.left.My = root.point[1]
			root.left.mz = root.mz
			root.left.Mz = root.Mz
		if(root.right!=None):
			root.right.mx = root.mx
			root.right.Mx = root.Mx
			root.right.my = root.point[1]
			root.right.My = root.My
			root.right.mz = root.mz
			root.right.Mz = root.Mz
	else:
		if(root.left!=None):
			root.left.mx = root.mx
			root.left.Mx = root.Mx
			root.left.my = root.my
			root.left.My = root.My
			root.left.mz = root.mz
			root.left.Mz = root.point[2]
		if(root.right!=None):
			root.right.mx = root.mx
			root.right.Mx = root.Mx
			root.right.my = root.my
			root.right.My = root.My
			root.right.mz = root.point[2]
			root.right.Mz = root.Mz

	limi(root.left)
	limi(root.right)

#Aqui tambien recorremos el arbol para sacar los limites y saber
#de donde a donde dibujar la linea divisora
def agreg(root):
	if(root==None):
		return
	if(root.left!=None):
		pi = plane(root.left)
		v.append(pi)
		aa=root.left.point
		ap=Punto(aa,root.axis)
		pp.append(ap)
	if(root.right!=None):
		pi = plane(root.right)
		v.append(pi)
		aa=root.right.point
		ap=Punto(aa,root.axis)
		pp.append(ap)
	agreg(root.left)
	agreg(root.right)

def grafi(node):
    if(node==None):
        return
    if(node.left!=None):
        text=" ".join(str(x) for x in node.left.point)
        text2=" ".join(str(x) for x in node.point)
        G.add_node(text)
        G.add_node(text2)
        G.add_edge(text2,text)
    if(node.right!=None):
        text=" ".join(str(x) for x in node.right.point)
        text2=" ".join(str(x) for x in node.point)
        G.add_node(text)
        G.add_node(text2)
        G.add_edge(text2,text)
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
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)



#Cremos una lista con valores aleatorios para hacer el kdtree
points=[]
for i in range (10):
	x=random.randint(0, 100)
	y=random.randint(0, 100)
	z=random.randint(0, 100)
	points.append([x,y,z])
#points=[(7,2,1), (5,4,2), (9,6,3), (4,7,4), (8,1,5), (2,3,6)]
#Construimosl arbol
root=build_kdtree(points)

grafi(root)
text=" ".join(str(x) for x in root.point)
pos = hierarchy_pos(G,text)
nx.draw(G, pos=pos, node_size=2000,with_labels=True)
plt.savefig('arbol.png')

#seteamos los limites iniciales despues de conocer la raiz
root.mx=0
root.Mx=100
root.my=0
root.My=100
root.mz=0
root.Mz=100
#sacamos los limites
limi(root)
#Le mandamos a v los valores para construir la primera linea
pi=plane(root)
v.append(pi)
#Le asignamos a esta el color azul
aa=root.point
ap=Punto(aa,0)
pp.append(ap)
agreg(root)
print(len(v))
#i sera nuestro iterador de los puntos
i=0
	
ren = vtkRenderer()
ren.SetBackground(0, 0, 0)

color=[255,255,255]
cube = vtkCubeSource()
cube.SetYLength(0.5)
cube.SetXLength(100)
cube.SetZLength(100)
cube.SetCenter(50,0,50)

cubeMapper = vtkPolyDataMapper()
cubeMapper.SetInputConnection(cube.GetOutputPort())
cubeMapper.SetResolveCoincidentTopologyToShiftZBuffer()
cubeActor = vtkActor()
cubeActor.SetMapper(cubeMapper)
cubeActor.GetProperty().SetColor(color)
cubeActor.GetProperty().SetOpacity(0.5)

cube2 = vtkCubeSource()
cube2.SetYLength(100)
cube2.SetXLength(0.5)
cube2.SetZLength(100)
cube2.SetCenter(0,50,50)

cubeMapper2 = vtkPolyDataMapper()
cubeMapper2.SetInputConnection(cube2.GetOutputPort())
cubeMapper2.SetResolveCoincidentTopologyToShiftZBuffer()
cubeActor2 = vtkActor()
cubeActor2.SetMapper(cubeMapper2)
cubeActor2.GetProperty().SetColor(color)
cubeActor2.GetProperty().SetOpacity(0.5)

cube3 = vtkCubeSource()
cube3.SetYLength(100)
cube3.SetXLength(100)
cube3.SetZLength(0.5)
cube3.SetCenter(50,50,0)

cubeMapper3 = vtkPolyDataMapper()
cubeMapper3.SetInputConnection(cube3.GetOutputPort())
cubeMapper3.SetResolveCoincidentTopologyToShiftZBuffer()
cubeActor3 = vtkActor()
cubeActor3.SetMapper(cubeMapper3)
cubeActor3.GetProperty().SetColor(color)
cubeActor3.GetProperty().SetOpacity(0.5)

ren.AddActor(cubeActor)
ren.AddActor(cubeActor2)
ren.AddActor(cubeActor3)

for punti in pp:
	ren.AddActor(punti.puntActor)



renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName("Kd-Tree")
renWin.SetSize(500,500)

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

def KeyPress(obj,event):
	global v
	global i
	global pp
	key = obj.GetKeySym()
	if(key=="Left"):
		if(i < len(v)):
			ren.AddActor(v[i].cubeActor)
			pp[i].puntActor.GetProperty().SetColor(v[i].color)
			pp[i].punt.SetRadius(1.5)
			print(pp[i].l)
			i=i+1
			iren.Render()
		else:
			for act in v:
				ren.RemoveActor(act.cubeActor)
			for act in pp:
				act.puntActor.GetProperty().SetColor([255,255,255])
				act.punt.SetRadius(1)
			i=0
			print("-------------------------------------------------")
			iren.Render()


iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
iren.AddObserver("KeyPressEvent", KeyPress)

iren.Initialize()
iren.Start()


print(root.point)
