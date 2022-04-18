import random

class Agenda:
    
    hr_inicio = 8
    hr_fin = 24
    
    def __init__(self):
        self.tareas = []
        self.puntero = 0
    
    def insertarTarea (self, tarea):
        if((tarea.h_comienzo >= self.hr_inicio) & ((tarea.h_comienzo + tarea.duracion) <= self.hr_fin)):
            if(self.estaLibreHorario(tarea)):
                self.tareas.append((tarea.h_comienzo, tarea.h_comienzo+tarea.duracion,  tarea))
            else:
                tarea.envejecimiento += 1
        else:
            if((tarea.h_caducidad >= self.hr_inicio) & (tarea.h_caducidad <= self.hr_fin)):
                if(self.hayLugar(tarea) & (self.puntero <= tarea.h_caducidad)):
                    self.tareas.append((self.puntero, self.puntero+tarea.duracion, tarea))
                else:
                    tarea.envejecimiento += 1   
            else:
                if(self.hayLugar(tarea)):
                    self.tareas.append((self.puntero, self.puntero+tarea.duracion, tarea))
        self.tareas.sort(key = lambda x:x[0])

    def estaLibreHorario(self, tarea):
        for x in self.tareas:
            tarea_final = tarea.h_comienzo + tarea.duracion
            if((x[0]==tarea.h_comienzo) |
               (x[1]==tarea.h_caducidad) |
               ((x[0]<tarea.h_comienzo) & (x[1]>tarea.h_comienzo)) |
               ((x[0]<tarea_final) & (x[1]>tarea_final)) |
               ((tarea.h_comienzo<x[0]) & (tarea_final>x[0])) |
               ((tarea.h_comienzo<x[1]) & (tarea_final>x[1]))):
                return False
        return True

    def hayLugar(self,tarea):
        if(len(self.tareas)> 0):
            if((self.tareas[0][0]-self.hr_inicio)>=tarea.duracion):
                self.puntero = self.hr_inicio
                return True
            else:
                for i in range (len(self.tareas)-1):
                    tiempoLibre = self.tareas[i+1][0] - self.tareas[i][1]
                    if(tiempoLibre>=tarea.duracion):
                        self.puntero = self.tareas[i][1]
                        return True
                if((self.hr_fin-self.tareas[len(self.tareas)-1][1])>=tarea.duracion):
                    self.puntero = self.tareas[len(self.tareas)-1][1]
                    return True
                else:
                    return False
        else:
            self.puntero = self.hr_inicio
            return True
        
    def insertarCola(self,tareas):
        for x in tareas:
            self.insertarTarea(x)

    def insertarMLQ(self,mlq):
        for x in mlq.getMLQ():
            for y in x:
                self.insertarTarea(y)

    def calcularPeso(self):
        puntajeAgenda = 0
        pts_urgencia = 15
        pts_importancia = 10
        pts_tipificacion = 2
        pts_porComienzo = 2
        pts_porFinal = 2
        for tarea in self.tareas:
            importancia = tarea[2].prioridad + tarea[2].envejecimiento
            if(importancia>3):
                importancia = 3
            puntajeTarea = 0    
            puntajeTarea += tarea[2].urgencia * pts_urgencia
            puntajeTarea += importancia * pts_importancia
            puntajeTarea += tarea[2].tipificacion * pts_tipificacion
            puntajeTarea += pts_porComienzo if(tarea[2].h_comienzo != 0) else 0
            puntajeTarea += pts_porFinal if(tarea[2].h_caducidad!= 0) else 0
            puntajeTarea += tarea[2].duracion
            puntajeAgenda += puntajeTarea
        return puntajeAgenda
            
    def getTareas(self):
        return self.tareas
    
    def imprimir(self):
        for x in self.tareas:
            print(str(x[0])+", "+ str(x[1])+" - "+str(x[2])) 
        

class Tarea:
    
    def __init__(self, nombre, duracion, h_caducidad, h_comienzo, prioridad, urgencia, tipicacion, envejecimiento):
        self.nombre = nombre
        self.duracion = duracion
        self.h_caducidad = h_caducidad
        self.h_comienzo = h_comienzo
        self.prioridad = prioridad
        self.urgencia = urgencia
        self.tipificacion = tipicacion
        self.envejecimiento = envejecimiento

    @staticmethod
    def generarTarea():
        finRangoComienzo = 60   #se puede cambiar este rango para variar la probabilidad de obtener una tarea con hora de comienzo
        finRangoCaducidad = 60  #se puede cambiar este rango para variar la probabilidad de obtener una tarea con hora de caducidad
        nombre = "T"+ str(random.randint(0,9999))
        duracion = random.randint(1,3)
        horario = range (Agenda.hr_inicio,Agenda.hr_fin)
        h_comienzo = random.randint(0,finRangoComienzo)
        h_comienzo = h_comienzo if (h_comienzo in horario) else 0
        h_caducidad = random.randint(0,finRangoCaducidad)
        h_caducidad = h_caducidad if ((h_caducidad in horario)&(h_comienzo == 0)) else 0   
        prioridad = random.randint(1,3)
        urgencia = random.randint(0,1)
        tipificacion = random.randint(1,3)
        envejecimiento = random.randint(0,2)
        return Tarea(nombre, duracion, h_caducidad, h_comienzo, prioridad, urgencia, tipificacion, envejecimiento)

    @staticmethod
    def generarTareas():
        randomTareas = []
        cantidadTareas = random.randint(5,20)
        for x in range(1, cantidadTareas):
            randomTareas.append(Tarea.generarTarea())
        return randomTareas

    def __str__(self):
        return self.nombre

class MLQ:

    def __init__(self):
        self.urg = []
        self.nourgprioridad3 = []
        self.nourgprioridad2 = []
        self.nourgprioridad1 = []
    
    def insertarEnMLQ(self,tarea):
        importancia = tarea.prioridad + tarea.envejecimiento
        if(importancia>3):
            importancia = 3
        if(tarea.urgencia>0):
            self.urg.append(tarea)
            self.urg.sort(key = lambda x : (x.prioridad, x.tipificacion), reverse = True)
        elif(importancia==3):
            self.nourgprioridad3.append(tarea)
            self.nourgprioridad3.sort(key = lambda x : x.tipificacion, reverse = True)
        elif(importancia==2):
            self.nourgprioridad2.append(tarea)
            self.nourgprioridad2.sort(key = lambda x : x.tipificacion, reverse = True)
        elif(importancia==1):
            self.nourgprioridad1.append(tarea)
            self.nourgprioridad1.sort(key = lambda x : x.tipificacion, reverse = True)

    def insertarColaEnMLQ(self, tareas):
        for tarea in tareas:
            self.insertarEnMLQ(tarea)
            
    def getMLQ(self):
        return [self.urg, self.nourgprioridad3, self.nourgprioridad2, self.nourgprioridad1]

a = 0
def ejecucion():
    global a
    
    a1 = Agenda()  
    a2 = Agenda()
    cola = Tarea.generarTareas()
    mlq = MLQ()
    mlq.insertarColaEnMLQ(cola)
    a1.insertarCola(cola)
    a2.insertarMLQ(mlq)

    if(a1.calcularPeso()>a2.calcularPeso()):
        a+=1

    #Muestra el contenido de la FIFO y la MLQ con sus respectivas agendas
    """
    print("Cantidad de actividades " + str(len(cola)))
    print()
    print("FIFO:")
    for x in cola:
        print("Nombre: "+x.nombre+" - Urgencia: "+str(x.urgencia) +" - Prioridad "  + str(x.prioridad) +" - Envejecimiento: " +str(x.envejecimiento)+" - Tipificación: "+str(x.tipificacion)+" - Hora comienzo: "+str(x.h_comienzo) +" - Hora caducidad: "+str(x.h_caducidad))
    print()
    print("MLQ:")
    i = 4
    for x in mlq.getMLQ():
        print(i)
        for y in x:
            print("Nombre: "+y.nombre+" - Urgencia: "+str(y.urgencia)+" - Prioridad " + str(y.prioridad) +" - Envejecimiento: " +str(y.envejecimiento)+" - Tipificación: "+str(y.tipificacion)+" - Hora comienzo: "+str(y.h_comienzo) +" - Hora caducidad: "+str(y.h_caducidad))
        print()
        i-=1
    print()
    print("Agenda FIFO:")
    a1.imprimir()
    print("\nAgenda MLQ:")
    a2.imprimir()
    print()
    """

    #Salida de archivo
    """
    separador = "\n"
    
    archivoFIFO = open("datosFIFO1000.csv","a+")
    archivoFIFO.write(str(a1.calcularPeso())+separador)
    archivoFIFO.close()
        
    archivoMLQ = open("datosMLQ1000.csv","a+")
    archivoMLQ.write(str(a2.calcularPeso())+separador)
    archivoFIFO.close()
    """
        
cantidadDeSimulaciones = 1000
for i in range(1, cantidadDeSimulaciones):
    ejecucion()

print("Casos simulados: " + str(cantidadDeSimulaciones))
print("Casos en los que MLQ es mejor: " + str(cantidadDeSimulaciones - a) + " casos - " + str((cantidadDeSimulaciones-a)*100/cantidadDeSimulaciones)+"% del total")
print("Casos en los que FIFO es mejor: " + str(a) + " casos - " + str(a*100/cantidadDeSimulaciones)+"% del total")
