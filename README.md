# gRPC_testing_aluvion

TIP: Usar este comando para instalar todo
=> pip install -r requirements.txt

No olvidar crear el típico .env (al menos con PORT y SERVER_ADDRESS)

PARA CONECTARSE A UN SERVIDOR EN OTRO COMPUTADOR, AÑADIR LA IP A SERVER_ADDRESS EN EL ARCHIVO .env
(ejemplo: SERVER_ADDRESS=192.168.1.88)

PARA PROBAR LA CONEXIÓN EN EL MISMO COMPUTADOR => SERVER_ADDRESS=localhost

TIP Raspberry PI OS:
=> ifconfig
Este comando permite conocer la dirección ip del "raspi".
Buscar el item "eth0" para la ip en localhost y así enviar peticiones a un servidor en la misma red local

OJO TIP
En general, las máquinas en la misma red comparten la IP local con una diferencia en el último valor
192.168.1.86
192.168.1.87
192.168.1.88