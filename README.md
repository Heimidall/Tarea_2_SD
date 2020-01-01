# Tarea 2 Sistemas Distribuidos

### Ejercicio 2

Para la ejecución del ejercicio 2 de esta tarea es necesario abrir una terminal dentro de la carpeta Ejercicio_2 y ejecutar los siguientes comandos:

>Docker-compose build

>Docker-compose up --scale consumer=2 

Con estos comandos se inicia la arquitectura con un servidor y dos clientes.
### Agregar mas clientes

Si se desea agregar mas clientes a la arquitectura es necesario el siguiente comando:
>Docker-compose up --scale consumer=N , donde N es la cantidad de clientes que se quiera tener.
### Ingresar valores por consola

Para ingresar valores a través de la consola con docker es necesario hacer abrir una nueva terminal, en la cual se debe ingresar el siguiente comando:
> Docker attach <Nombre del container>
  
Este proceso se debe repetir para la cantidad de terminales en las cuales desee ingresar valores.
