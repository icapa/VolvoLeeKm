#!/usr/bin/python

import time
import serial

secuencia=[
'ATZ',
'ATL1',
'ATE0',
'ATSP 3', 
'ATH1',
'ATAL',
'ATKW0',
'ATTA 13',
'ATRA 13',           
'ATIIA 51',
'ATWM 82 51 13 A1',
'ATSI',              
'ATSH 84 51 13',
'B90300'
]



#Funcion que abre el puerto
def AbrePuerto():
	ser = serial.Serial()
	ser.port = '/dev/cu.usbserial-A400f2at'
	#Linux ser.port='/dev/ttyUSB0'
	ser.baudrate=38400	
	ser.timeout=2
	
	ser.open()
	return ser

#Funcion que envia un comando y retorna la respuesta
def EnviaComando(comando,ser):
	ser.write(comando+'\r\n')
	out=''
	dato='a'
	while (dato !=''):
		dato=ser.read(1)
		if (len(dato)==1):
			out+=dato
	#print "Linea= "+ str(len(out))
	return out


#Lista los comandos
def ListaComandos(comandos):
	for i in range(len(comandos)):
		print "Comando: ",i+1,"\t",comandos[i]



def CalculaKm(trama):
	bytesSeparados=trama.split(' ')
	print "Numero de bytes : " + str(len(bytesSeparados)) 
	for i in range(len(bytesSeparados)):
		print "Byte: " + str(i) + "=>" + bytesSeparados[i]
	if(len(bytesSeparados)>=8 and bytesSeparados[0]=='85'):
		km=int(bytesSeparados[6]+bytesSeparados[5],16)*10
		return km
	else:
		return 0

#
puertoSerie=AbrePuerto()

for i in range(len(secuencia)):
	print "Preguntando secuencia " + secuencia[i] +" -> "+ str(i) +  "\r\n------------------\r\n"
	laTrama=EnviaComando(secuencia[i],puertoSerie)
	print "Leido: " + laTrama
	losKm=0
	if (i==13):
		tramaPartida=laTrama.split('\r')
		numCachos =len(tramaPartida)
		for j in range (len(tramaPartida)):
			print "Partida trama: " + str(j) + "-->" + tramaPartida[j]
		#print "Trama correcta " + str(numCachos)
		losKm=CalculaKm(tramaPartida[0])
		print "Los km del Volvo 850 son: ",losKm


puertoSerie.close()
