import vtk
import random

class Punto:
    def __init__(self,x,y,z,dato):
        self.x=x
        self.y=y
        self.z=z
        self.dato=dato

class Prisma:
    def __init__(self,x,y,z,l,h,a):
        self.ancho=a
        self.largo=l
        self.alto=h
        self.x=x
        self.y=y
        self.z=z
    def Contiene(self,punto):
        return(punto.x<=self.x+self.largo and punto.x>=self.x-self.largo and punto.y<=self.y+self.alto and punto.y>=self.y-self.alto and punto.z<=self.z+self.ancho and punto.z>=self.z-self.ancho)

    def intersects(self,range):
                    if ((range.x-range.t>self.x-self.t and range.x-range.t<self.x+self.t) or (range.x-range.t<self.x-self.t and self.x-self.t<range.x+range.t)):
                            if ((range.y-range.t>self.y-self.t and range.y-range.t<self.y+self.t) or (range.y-range.t<self.y-self.t and self.y-self.t<range.y+range.t)):
                                    return (range.z-range.t>self.z-self.t and range.z-range.t<self.z+self.t) or (range.z-range.t<self.z-self.t and self.z-self.t<range.z+range.t)
                    return False
    def Intersecta(self,prisma):

        if ((prisma.x-prisma.largo>self.x-self.largo and prisma.x-prisma.largo<self.x+self.largo) or (prisma.x-prisma.largo<self.x-self.largo and self.x-self.largo<prisma.x+prisma.largo)):
            if ((prisma.y-prisma.alto>self.y-self.alto and prisma.y-prisma.alto<self.y+self.alto) or (prisma.y-prisma.alto<self.y-self.alto and self.y-self.alto<prisma.y+prisma.alto)):
                
                return (prisma.z-prisma.ancho>self.z-self.ancho and prisma.z-prisma.ancho<self.z+self.ancho) or (prisma.z-prisma.ancho<self.z-self.ancho and self.z-self.ancho<prisma.z+prisma.ancho)
        
        return False

class OcTree:
    def __init__(self,contorno,capacidad):
        self.contorno=contorno
        self.capacidad=capacidad
        self.puntos=[]
        self.dividido=False
        
    def g(self,dato):
        if(dato=="x"):
            return self.contorno.x
        elif(dato=="y"):
            return self.contorno.y
        elif(dato=="z"):
            return self.contorno.z
        elif(dato=="a"):
            return self.contorno.ancho
        elif(dato=="l"):
            return self.contorno.largo
        elif(dato=="h"):
            return self.contorno.alto
        
    def Dividir(self):
       
        f_no=Prisma(self.g('x')-self.g('l')/2,self.g('y')-self.g('h')/2,self.g('z')+self.g('a')/2,self.g('l')/2,self.g('h')/2,self.g('a')/2)
        f_ne=Prisma(self.g('x')+self.g('l')/2,self.g('y')-self.g('h')/2,self.g('z')+self.g('a')/2,self.g('l')/2,self.g('h')/2,self.g('a')/2)
        f_so=Prisma(self.g('x')-self.g('l')/2,self.g('y')+self.g('h')/2,self.g('z')+self.g('a')/2,self.g('l')/2,self.g('h')/2,self.g('a')/2)
        f_se=Prisma(self.g('x')+self.g('l')/2,self.g('y')+self.g('h')/2,self.g('z')+self.g('a')/2,self.g('l')/2,self.g('h')/2,self.g('a')/2)
        
        b_no=Prisma(self.g('x')-self.g('l')/2,self.g('y')-self.g('h')/2,self.g('z')-self.g('a')/2,self.g('l')/2,self.g('h')/2,self.g('a')/2)
        b_ne=Prisma(self.g('x')+self.g('l')/2,self.g('y')-self.g('h')/2,self.g('z')-self.g('a')/2,self.g('l')/2,self.g('h')/2,self.g('a')/2)
        b_so=Prisma(self.g('x')-self.g('l')/2,self.g('y')+self.g('h')/2,self.g('z')-self.g('a')/2,self.g('l')/2,self.g('h')/2,self.g('a')/2)
        b_se=Prisma(self.g('x')+self.g('l')/2,self.g('y')+self.g('h')/2,self.g('z')-self.g('a')/2,self.g('l')/2,self.g('h')/2,self.g('a')/2)

        self.Hijof_no=OcTree(f_no,self.capacidad)
        self.Hijof_ne=OcTree(f_ne,self.capacidad)
        self.Hijof_so=OcTree(f_so,self.capacidad)
        self.Hijof_se=OcTree(f_se,self.capacidad)

        self.Hijob_no=OcTree(b_no,self.capacidad)
        self.Hijob_ne=OcTree(b_ne,self.capacidad)
        self.Hijob_so=OcTree(b_so,self.capacidad)
        self.Hijob_se=OcTree(b_se,self.capacidad)

        self.dividido=True
        
    def Insertar(self,punto):
        if(not self.contorno.Contiene(punto)):
            return False
        if(len(self.puntos)<self.capacidad):
            self.puntos.append(punto)
        else:
            if(not self.dividido):
                self.Dividir()
            self.Hijof_no.Insertar(punto)
            self.Hijof_ne.Insertar(punto)
            self.Hijof_so.Insertar(punto)
            self.Hijof_se.Insertar(punto)
            self.Hijob_no.Insertar(punto)
            self.Hijob_ne.Insertar(punto)
            self.Hijob_so.Insertar(punto)
            self.Hijob_se.Insertar(punto)
        return True
    def Consulta(self,prisma,respuesta):
        global total
        if(not self.contorno.Intersecta(prisma)):
            #print("A")
            return 
        #print("cubo",self.contorno.x,self.contorno.y,self.contorno.z)
        #print(self.contorno.largo)
        
        #print("B")
        for i in self.puntos:
            if(prisma.Contiene(i)):
                respuesta.append(i)
            total+=1
        if(self.dividido):
            self.Hijof_no.Consulta(prisma,respuesta)
            self.Hijof_ne.Consulta(prisma,respuesta)
            self.Hijof_so.Consulta(prisma,respuesta)
            self.Hijof_se.Consulta(prisma,respuesta)
            self.Hijob_no.Consulta(prisma,respuesta)
            self.Hijob_ne.Consulta(prisma,respuesta)
            self.Hijob_so.Consulta(prisma,respuesta)
            self.Hijob_se.Consulta(prisma,respuesta)
   
        
    def Mostrar(self,color):
        global vec
        cube = vtk.vtkCubeSource()
        cube.SetCenter(0,0,0)
        cubeMapper = vtk.vtkPolyDataMapper()
        cubeActor = vtk.vtkActor()
        cube.SetXLength(self.g('l')*2)
        cube.SetYLength(self.g('h')*2)
        cube.SetZLength(self.g('a')*2)
        cubeMapper.SetInputConnection(cube.GetOutputPort())
        
        cubeActor.SetMapper(cubeMapper)
        cubeActor.SetPosition(self.g('x'),self.g('y'),self.g('z'))
        cubeActor.GetProperty().SetColor(colores[color][0],colores[color][1],colores[color][2])
        cubeActor.GetProperty().SetOpacity(0.2)
        ren.AddActor(cubeActor)
        vec.append(cubeActor)
        GraficarPuntos(self.puntos,colores[color],False)
        
        if(self.dividido):
            self.Hijof_no.Mostrar(0)
            self.Hijof_ne.Mostrar(1)
            self.Hijof_so.Mostrar(2)
            self.Hijof_se.Mostrar(3)
            
            self.Hijob_no.Mostrar(4)
            self.Hijob_ne.Mostrar(5)
            self.Hijob_so.Mostrar(6)
            self.Hijob_se.Mostrar(7)
    def print(self):
        print(self.contorno.alto)
        for i in self.puntos:
            print(i.x,i.y,i.z)
        
        if(self.dividido):
            self.Hijof_no.print()
            self.Hijof_ne.print()
            self.Hijof_so.print()
            self.Hijof_se.print()
                
            self.Hijob_no.print()
            self.Hijob_ne.print()
            self.Hijob_so.print()
            self.Hijob_se.print()
            
            
def GraficarPuntos(puntos=[],color=[0,0,0],consulta=False):
    esferaMapper=[]
    esferas=[]
    esferaactor = []
    i=0
    txtMapper=[]
    txt=[]
    txtActor = []
    for punto in puntos:
        esferaMapper.append(vtk.vtkPolyDataMapper())
        esferas.append(vtk.vtkSphereSource())
        esferaactor.append(vtk.vtkActor())
        esferas[i].SetCenter(punto.x,punto.y,punto.z)
        esferas[i].SetRadius(2)
        esferaMapper[i].SetInputConnection(esferas[i].GetOutputPort())
        esferaactor[i].SetMapper(esferaMapper[i])
        esferaactor[i].GetProperty().SetOpacity(1)
        esferaactor[i].GetProperty().SetColor(color[0],color[1],color[2])
        ren.AddActor(esferaactor[i])
        vec.append(esferaactor[i])
        if(consulta):
            txtMapper.append(vtk.vtkPolyDataMapper())
            txt.append(vtk.vtkVectorText())
            txt[i].SetText(str(i+1))
            txtMapper[i].SetInputConnection(txt[i].GetOutputPort())
            txtActor.append(vtk.vtkFollower())
            txtActor[i].SetMapper(txtMapper[i])
            txtActor[i].SetScale(2.5, 2.5, 2.5)
            txtActor[i].AddPosition(punto.x-2,punto.y-2,punto.z+2)
            txtActor[i].GetProperty().SetColor(255,255,255)
            ren.AddActor(txtActor[i])
            vec.append(txtActor[i])
            
        i+=1
    return esferaactor,txtActor



def KeyPress(obj,event):
    global vec
    global OT
    global cubeActor
    global aux
    global aux2
    key = obj.GetKeySym()
    if(aux==None):
        print()
    elif(len(aux)>0):
        for i in aux:
            ren.RemoveActor(i)
        for i in aux2:
            ren.RemoveActor(i)
    if(key=="8"):
        posi=cubeActor.GetPosition()
        posi_n=[posi[0],posi[1]+1.0,posi[2]]
        cubeActor.SetPosition(posi_n)
        respuesta=[]
        OT.Consulta(Prisma(posi_n[0],posi_n[1],posi_n[2],cube.GetXLength()/2,cube.GetYLength()/2,cube.GetZLength()/2),respuesta)
        aux,aux2=GraficarPuntos(respuesta,[0,0,0],True)
        iren.Render()
    elif(key=="5"):
        posi=cubeActor.GetPosition()
        posi_n=[posi[0],posi[1]-1.0,posi[2]]
        cubeActor.SetPosition(posi_n)
        respuesta=[]
        OT.Consulta(Prisma(posi_n[0],posi_n[1],posi_n[2],cube.GetXLength()/2,cube.GetYLength()/2,cube.GetZLength()/2),respuesta)
        aux,aux2=GraficarPuntos(respuesta,[0,0,0],True)
        iren.Render()
    elif(key=="4"):
        posi=cubeActor.GetPosition()
        posi_n=[posi[0]-1.0,posi[1],posi[2]]
        cubeActor.SetPosition(posi_n)
  
        respuesta=[]
        OT.Consulta(Prisma(posi_n[0],posi_n[1],posi_n[2],cube.GetXLength()/2,cube.GetYLength()/2,cube.GetZLength()/2),respuesta)
        aux,aux2=GraficarPuntos(respuesta,[0,0,0],True)
        iren.Render()
    elif(key=="6"):
        posi=cubeActor.GetPosition()
        posi_n=[posi[0]+1.0,posi[1],posi[2]]
        cubeActor.SetPosition(posi_n)
   
        respuesta=[]
        OT.Consulta(Prisma(posi_n[0],posi_n[1],posi_n[2],cube.GetXLength()/2,cube.GetYLength()/2,cube.GetZLength()/2),respuesta)
        aux,aux2=GraficarPuntos(respuesta,[0,0,0],True)
        iren.Render()
    elif(key=="7"):
        posi=cubeActor.GetPosition()
        posi_n=[posi[0],posi[1],posi[2]+1.0]
        cubeActor.SetPosition(posi_n)

        respuesta=[]
        OT.Consulta(Prisma(posi_n[0],posi_n[1],posi_n[2],cube.GetXLength()/2,cube.GetYLength()/2,cube.GetZLength()/2),respuesta)
        aux,aux2=GraficarPuntos(respuesta,[0,0,0],True)
        iren.Render()
    elif(key=="9"):
        posi=cubeActor.GetPosition()
        posi_n=[posi[0],posi[1],posi[2]-1.0]
        cubeActor.SetPosition(posi_n)
        respuesta=[]
        OT.Consulta(Prisma(posi_n[0],posi_n[1],posi_n[2],cube.GetXLength()/2,cube.GetYLength()/2,cube.GetZLength()/2),respuesta)
        aux,aux2=GraficarPuntos(respuesta,[0,0,0],True)
        iren.Render()
    elif(key=="i"):
        cube.SetYLength(cube.GetYLength()+1)
        iren.Render()   
    elif(key=="k"):
        cube.SetYLength(cube.GetYLength()-1)
        iren.Render()
    elif(key=="j"):
        cube.SetXLength(cube.GetXLength()+1)
        iren.Render()
    elif(key=="l"):
        cube.SetXLength(cube.GetXLength()-1)
        iren.Render()
    elif(key=="u"):
        cube.SetZLength(cube.GetZLength()+1)
        iren.Render()
    elif(key=="o"):
        cube.SetZLength(cube.GetZLength()-1)
        iren.Render()
    elif(key=="h"):
        print("Ingrese coordenadas del nuevo punto")
        x=int(input("Eje X: "))
        y=int(input("Eje Y: "))
        z=int(input("Eje Z: "))
        OT.Insertar(Punto(x,y,z,0))
        limpiar()
        OT.Mostrar(0)
    
    
def CrearConsulta():
    
    cube.SetXLength(20)
    cube.SetYLength(20)
    cube.SetZLength(20)
    cubeMapper=vtk.vtkPolyDataMapper()
    cubeMapper.SetInputConnection(cube.GetOutputPort())
    
    cubeActor.GetProperty().SetColor(255,0,0)
    cubeActor.GetProperty().SetOpacity(0.5)
    cubeActor.SetMapper(cubeMapper)
    cubeActor.SetPosition(65,65,65)
    ren.AddActor(cubeActor)
def InsertarAleatorio(n):
    global OT
    
    for i in range(n):
        OT.Insertar(Punto(random.uniform(-50,50),random.uniform(-50,50),random.uniform(-50,50),i))
    OT.Mostrar(0)
def limpiar():
    global vec
    global ren
    print(len(vec))
    for i in vec:
        ren.RemoveActor(i)
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
c =Prisma(0,0,0,50,50,50)
OT =OcTree(c,4)
cube=vtk.vtkCubeSource()
cubeActor=vtk.vtkActor()
total=0
aux=[ ]
aux2=[ ]
vec=[]
colores=[[255,225,0],[190,110,35],[45,255,0],[0,255,175],[0,80,255],[110,0,255],[255,0,230],[100,155,145]]

def main():
    
    renWin.AddRenderer(ren)
    renWin.SetWindowName("Octree")
    renWin.SetSize(1300, 680)
    ren.SetBackground(255,255,255)
    iren.AddObserver("KeyPressEvent",KeyPress)
    iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    
    InsertarAleatorio(100)
    CrearConsulta()
    iren.Initialize()
    renWin.Render()
    iren.Start()

main()


