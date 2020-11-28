import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from random import choice
import time
import csv

def BubbleSort(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n-i-1):
            if lista[j] > lista[j+1] :
                lista[j], lista[j+1] = lista[j+1], lista[j]

def InsertSort(A):
    for i in range(len(A)): 
        min_idx = i 
        for j in range(i+1, len(A)): 
            if A[min_idx] > A[j]: 
                min_idx = j 
        A[i], A[min_idx] = A[min_idx], A[i]
        
def CountSort(lista):
    ma=max(lista)
    mi=min(lista)
    rango=ma-mi+1
    count=[0 for i in range(rango)]
    output =[0 for i in range(len(lista))]
    for i in lista: 
        count[i-mi] += 1
    for i in range(1,rango): 
        count[i] += count[i-1] 
    for i in range(len(lista)-1,-1,-1): 
        output[count[lista[i]-mi]-1] = lista[i] 
        count[lista[i]-mi] -= 1
    for i in range(len(lista)): 
        lista[i] = output[i] 
   # return ans


def heapify(lista, n, i): 
    largest = i  
    l = 2 * i + 1  
    r = 2 * i + 2  
    if l < n and lista[i] < lista[l]: 
        largest = l 
    if r < n and lista[largest] < lista[r]: 
        largest = r 
    if largest != i: 
        lista[i],lista[largest] = lista[largest],lista[i] 
        heapify(lista, n, largest) 
def HeapSort(lista): 
    n = len(lista) 
    for i in range(n, -1, -1): 
        heapify(lista, n, i) 
    for i in range(n-1, 0, -1): 
        lista[i], lista[0] = lista[0], lista[i] 
        heapify(lista, i, 0)
def MergeSort(lista): 
    if len(lista) >1: 
        mid = len(lista)//2 
        L = lista[:mid] 
        R = lista[mid:]  
        MergeSort(L) 
        MergeSort(R) 
        i = j = k = 0
        while i < len(L) and j < len(R): 
            if L[i] < R[j]: 
                lista[k] = L[i] 
                i+=1
            else: 
                lista[k] = R[j] 
                j+=1
            k+=1
        while i < len(L): 
            lista[k] = L[i] 
            i+=1
            k+=1 
        while j < len(R): 
            lista[k] = R[j] 
            j+=1
            k+=1

def partition(lista,low,high): 
    i = ( low-1 )        
    pivot = lista[high]   
    for j in range(low , high): 
        if   lista[j] < pivot: 
            i = i+1 
            lista[i],lista[j] = lista[j],lista[i] 
    lista[i+1],lista[high] = lista[high],lista[i+1] 
    return ( i+1 )

def QuickSort(lista,low=0,high=-100):
    if(high==-100):
        high=len(lista)-1
    if low < high: 
        pi = partition(lista,low,high) 
        QuickSort(lista, low, pi-1) 
        QuickSort(lista, pi+1, high)
def SelectionSort(lista):
    for i in range(len(lista)):  
        min_idx = i 
        for j in range(i+1, len(lista)): 
            if lista[min_idx] > lista[j]: 
                min_idx = j       
        lista[i], lista[min_idx] = lista[min_idx], lista[i]
def tiempo(f,v):
    start = time.time()
    f( v )
    return (time.time() - start) *1000
def generarDatos(Ns = range(10,100,10), numTrials=20, listMax = 10, name='name.csv'):
    f=open(name,"w")
    for n in Ns:
        lst = [ choice(range(listMax)) for i in range(n) ]
        f.write(str(n)+";")
        f.write(str(tiempo(QuickSort,lst))+";")
        f.write(str(tiempo(BubbleSort,lst))+";")
        f.write(str(tiempo(CountSort,lst))+";")
        f.write(str(tiempo(HeapSort,lst))+";")
        f.write(str(tiempo(InsertSort,lst))+";")
        f.write(str(tiempo(MergeSort,lst))+";")
        f.write(str(tiempo(SelectionSort,lst))+";\n")
        
def cargar(name):

    L=["quickSort","bubbleSort","countSort","heapSort","insertionSort","mergeSort","selectionSort"]
    data=np.loadtxt(name,dtype=np.str,delimiter=';',unpack=True)
    x=data[0,:]
    for i in range(1,8):
        print(i)
        y=data[i,:]
        plt.plot(x,y,marker='.',label=L[i-1])
        #print(y)
    plt.legend()
    if name== "cplus.csv":
    	plt.title("C++")
    if name=="python.csv":
    	plt.title("Python")
    plt.show()

def algoritmo(name,pos):   
        data=np.loadtxt('cplus.csv',dtype=np.str,delimiter=';',unpack=True)
        x=data[0,:]
        y=data[pos,:]
        plt.plot(x, y, "-.", color="red", label="C++")

        data=np.loadtxt('python.csv',dtype=np.str,delimiter=';',unpack=True)
        x=data[0,:]
        y=data[pos,:]
        plt.plot(x, y, "-.", color="green", label="Python")
        
        
        data=np.loadtxt('java.csv',dtype=np.str,delimiter=';',unpack=True)
        x=data[0,:]
        y=data[pos,:]
        plt.plot(x, y, "-.", color="blue", label="Java")
        plt.legend()
        plt.title(name)
        plt.show()
                      
                    
   


    
    
"""
lista = [64, 34, 25, 12, 22, 11, 90]
#bubbleSort(lista)
#countSort(lista)
#heapSort(lista)
#insertionSort(lista)
#mergeSort(lista)
quickSort(lista)
#selectionSort(lista)
print ("Sorted listaay is:")
for i in range(len(lista)):
    print ("%d" %lista[i])



nValuesMerge, tValuesMerge = trySelectABunch(quickSort, Ns=nVals, numTrials=1, listMax = 1000)
plt.plot(nValuesMerge, tValuesMerge, "-.", color="pink", label="quickSort")

nValuesMerge, tValuesMerge = trySelectABunch(bubbleSort, Ns=nVals, numTrials=1, listMax = 1000)
plt.plot(nValuesMerge, tValuesMerge, "-.", color="red", label="bubbleSort")
nValuesMerge, tValuesMerge = trySelectABunch(countSort, Ns=nVals, numTrials=1, listMax = 1000)
plt.plot(nValuesMerge, tValuesMerge, "-.", color="green", label="countSort")
nValuesMerge, tValuesMerge = trySelectABunch(heapSort, Ns=nVals, numTrials=1, listMax = 1000)
plt.plot(nValuesMerge, tValuesMerge, "-.", color="yellow", label="heapSort")
nValuesMerge, tValuesMerge = trySelectABunch(insertionSort, Ns=nVals, numTrials=1, listMax = 1000)
plt.plot(nValuesMerge, tValuesMerge, "-.", color="black", label="insertionSort")
nValuesMerge, tValuesMerge = trySelectABunch(mergeSort, Ns=nVals, numTrials=1, listMax = 1000)
plt.plot(nValuesMerge, tValuesMerge, "-.", color="gray", label="mergeSort")

nValuesMerge, tValuesMerge = trySelectABunch(selectionSort, Ns=nVals, numTrials=1, listMax = 1000)
plt.plot(nValuesMerge, tValuesMerge, "-.", color="blue", label="selectionSort")
plt.xlabel("n")
plt.ylabel("Time(ms)")
plt.legend()
plt.title("Seleccion")

plt.show()
plt.savefig("1.png")
"""

#nVals = list( range(1000,11000,1000))
#generarDatos(Ns=nVals, numTrials=1, listMax = 1000,name='python.csv')
 
#cargar('java.csv')   
#cargar('python.csv')
cargar('cplus.csv')

L=["quickSort","bubbleSort","countSort","heapSort","insertionSort","mergeSort","selectionSort"]
#for i in range(1,len(L)+1):
#algoritmo(L[1],2)
    

