#### paquetes usados #####
from joblib import Parallel, delayed
from skimage import io, color
import csv
import cv2
import matplotlib.pyplot as plt
import multiprocessing
import numpy as np
import os
###########################

###### Funciones de analisis de imagen ######
def brillo(imagen):
    return "b"

def puntosBlancos(imagen):
    y = len(imagen)
    x = len(imagen[1])
    avg = np.zeros((y,x,3),dtype=int)
    avg_color = imagen.mean(axis=0).mean(axis=0)

    #for i in range(y):
    #    for j in range(x):
    #        avg[i][j][0]=round(avg_color[0])
    #        avg[i][j][1]=round(avg_color[1])
    #        avg[i][j][2]=round(avg_color[2])
    con = 0
    
    for i in range(y):
        for j in range(x):
            aux1 = (imagen[i][j][0]**2+imagen[i][j][1]**2+imagen[i][j][2]**2)**0.5
            if aux1*0.65 >= (avg_color[0]**2+avg_color[1]**2+avg_color[2]**2)**0.5:
                con += 1
    return con

def promedio(imagen):
    avg_color_per_row = np.average(imagen, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    return str(avg_color)

def metrica(imagen):
    return "m"

def colorDominante(imagen):
    test_list = []
    for i in range(len(imagen)):
        for j in range(len(imagen[i])):
            test_list.append(str(imagen[i][j]))
    max = 0
    res = test_list[0]
    print("cantidad de elementos: "+str(len(test_list)))
    for i in test_list:
        freq = test_list.count(i)
        for j in range(freq):
            test_list.remove(i)
        if freq > max:
            max = freq
            res = i
            print("nueva frecuencia: "+str(freq))
            print("cantidad de elementos: "+str(len(test_list)))
    return res
#############################################

########CONFIGURACIONES########

# Nombre archivo de salida
nombreArchivo = "resultados.csv"

# Delimitador para el archivo csv ("," o ";")
delimitador = ","

# lista de funciones a aplicar a cada imagen
# agregar el nombre de la funcion deseada sin commillas
# la funcion debe estar definida en "Funciones de analisis de imagen"
funciones = [puntosBlancos]
###############################

######## Funcion principal ########

def analisis(imagen, directorio):
    # resultados de cada funcion aplicada a la imagen
    resutadosPorImagen = []


    # dirección relativa de la imagen
    path = directorio+"/"+imagen

    # se lee la imagen
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # se agrega el numero de la imgagen al archivo csv resultante
    resutadosPorImagen.append(directorio)

    # analisis de la imagen
    for funcion in funciones:
        resutadosPorImagen.append(funcion.__call__(img))

    return resutadosPorImagen

###################################


# listar todos los archivos de la carpeta actual
archivos = os.listdir()

# lista que va a contener todas las carpetas
carpetas = []

for i in archivos:
    # si el el archivo es una carpeta se agrega a la lista de carpetas
    if os.path.isfile(i) != True and i[0]!=".":
        carpetas.append(i)

# ordenar las carpetas por numero de forma ascendente
carpetas.sort(key=int)

# csvFinal se usa para crear el archivo de reporte
csvFinal = []

# agregar titulos de las columnas
aux = ["Aguacate"]
for funcion in funciones:
    aux.append(funcion.__name__)
csvFinal.append(aux)

for carpeta in carpetas:
    imagenes = os.listdir(carpeta)
    imagenes = ["6_590nm.png"]
    print("carpeta: "+str(carpeta))

    num_cores = multiprocessing.cpu_count()

    results = Parallel(n_jobs=num_cores)(delayed(analisis)(i,carpeta) for i in imagenes)

    for resultado in results:
        csvFinal.append(resultado)

# crear el archivo de reporte
with open(nombreArchivo,"w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=delimitador)
    csvWriter.writerows(csvFinal)
