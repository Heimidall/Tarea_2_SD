Parte 1: Chat entre cliente y servidor
    - No se sabe cuanto clientes en total pueden ser pero tiene que saber una manera de poder ir agregandolos de manera dinámica, lo que se me ocurre es que vamos a tener 
    que crear procedures que sean del tipo, MesjCliente1
    MesjCliente2 para asi poder enviar mensajes a cada cliente todo esto manejado desde la consola.
    - En teoria el servidor deberia ser capaz de poder enviar mensajes a todos los clientes y cada cliente deberia poder solo mandar mensajes al servidor,
    el tema es que en el mesanje que le manda el cliente al servidor tiene que ir explicito o se debe definir una manera de poder saber a que cliente quiero mandarle el mensaje
    y que mensaje quiero mandar.
    onda del estilo sendMsj(Cliente1, "Este es el mensaje para el cliente1") entonces ese tipo de procedure debe estar dentro del server y podriamos acceder a ellos con
    opciones dentro de la consola solamente.
    - Hay que ver bien como hacer las cosas asincronas.


Parte 2:
    - Acá entonces se tiene que crear la imagen de docker para rabbit MQ? o se sigue usando python, ahi me perdí.

    ----------------------------------------------------------------------------------------------------------------------

    Puede ser que el server tenga un archivo con los clientes que se han ido creando o algo asi por el estilo, o que cada vez
    que se cree un cliente añada un campo a un archivo, de esa manera tienen para saber que "numero ponerse para el nombre de la queue"
    el nombre defaul que quiero ponerle a la queue debe ser del estilo cliente_X, donde X es el numero del cliente creando
    -------------------------------------------------------------------------------------------------------------------------
    Cada nodo que se cree debe ser tanto publisher como suscribe, por lo tanto debo tener una clase que sea publisher y otra que 
    sea suscribe, la idea sería que ambos metodos se creen en threads, así no quedan tomados el envio y/o recibida de mensajes.
    -----------------------------------------------------------------------------------------------------------------------------
    Antes de crear su cola el cliente debe enviar el mensaje al server, a ver el server que el "ID" del cliente es null, pero el cliente
    no va a poder recibir el mensaje de respuesta hasta que cree su propia queue, es por eso que quiza una opcion es que se cree con una cola
    fantasma para poder recibir el primer mensaje y luego cree nuevamente su cola con el mensaje nuevo 
    -------------------------------------------------------------------------------------------------------------------------------------------
    To do:
    - ~~Crear el servicio para mostrar la lista de los clientes completos.~~
    - ~~Agregar un ID a los mensajes~~
    - ~~Agregar el timestamp a los mensajes~~
    - ~~Cliente con ID_unico (Esto ya se hace con el nombre que se obtiene no?)~~ 
    - ~~Crear el servicio para obtener todos los mensajes enviados por el cliente. (Quiza esto sea bueno guardarlo de la misma manera como se hacen con los nombres de los clientes.)~~
    - ~~Crear un log.txt para mantener el registros de los mensajes que se envian a través del servidor.~~
    - Se debe agregar algo de validacion cuando no se ingresen las palabras correctas.
