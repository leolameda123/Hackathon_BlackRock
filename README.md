# Hackathon_BlackRock

Descripción General:

Este proyecto es la respuesta al Hackathon creador por Black Rock. Consiste en un API con cinco endpoints para calcular, de una serie de gastos, el posible retorno que generaría el posible ahorro e inversión del redondeo de los gastos. A continuación se describe la estrategia:

    *Redondeo de gastos: por cada gasto se redondea hacia el siguiente múltiplo de 100. El REMANENTE (redondeo - gasto) es la cantidad que será invertida  por cada gasto.

El remanente puede ser modificado con base a rangos de fechas donde se puede generar un remanente fijo, o agregar un extra al remanente.

Inversion del ahorro en dos opciones: 

    *ishares: interés anual del 7.11% con devolución de hasta el 10% del ingreso anual
    *Plan Personal de Retiro(PPR): interés anual del 14.49%, no genérela devolución

El rendimeinto de la inversión se calcula de la siguiente manera:

	A = P(1+(r/n))^nt 

    A = Rendimiento de la inversión 
    P = Monto invertido
    r = tasa de interes anual
    n = numero de veces que se aplica el interés al año
    t = tiempo de inversión considerando una edad de retiro de 65 años

Por útil se ajusta el rendimiento de la inversión a una tasa fija de inflación utilizando las formula:

	Af = A/(1+inflació)^t

    Af = Monto ajustado a la inflación 
    A = Monto del rendimiento de la inversión
    Inflación = % de inflación fija a considerar
    t = tiempo de inversión considerando una edad de retiro de 65 años

Los endpoints con los que cuenta el API son los siguientes:

    - Construcción de Transacciones - 
    Host/blackrock/challenge/v1/transactions:parse
	
	    Encargado de recibir una lista de transacciones, calcular y devolver la lista de transacciones incluyendo el remanente generado debido al redondeo.

    - Validador de Transacciones -
    Host/blackrock/challenge/v1/transactions:validator

        Recibe una lista de transacciones y las clasifica en transacciones validas e invalidas aplicando los siguientes criterios:

            -Transacciona duplicada
            -Monto de transacción igual a cero
            -Valores de remanentes correctos
            -Montos negativos 

        Devuelve una lista de transacciones válidas y otra de transacciones invalidas

    - Validador de Restricciones Temporales -
    Host/blackrock/challenge/v1/transactions:filter

        Recibe:
            - lista de transacciones
            - lista de periodos donde el remanente es fijo
            - lista de periodos donde se agrega un extra al remanente

        Si existe un superposición en los rangos fijos y extra, se prioriza el rango fijo y no se agrega el extra. Así como si existe un traslape entre rangos del mismo tipo, se prioriza el valor menor en la modificación del remanente.

        Devuelve una lista de transacciones validas y transacciones invalidas aplicando los criterios anteriores, agregando una validación adicional, que es el valor del remanente mayor a cero. 

    - Calculo de Rendimientos PPR -
    Host/blackrock/challenge/v1/returns:ppr
    Host/blackrock/challenge/v1/returns:ishares

        Recibe lista de datos para realizar le calculo de los rendimientos y devuelve los datos financieros de la inversión en rangos parciales y el rango total de la inversión

    - Reporte de Performance -
    Host/blackrock/challenge/v1/performance

        Devuelve los datos de tiempo de ejecución, memoria utilizada y numero de hilos de la aplicación al ejecutar el ultimo llamado al API


Descripción de la aplicación:

    La aplicación fue creada utilizando el lenguaje de programación Python y el Framework the Flask. Cuenta con un base de datos SQLite para guardar la informacion referente al ultimo llamado del API. Se despliega en un contenedor docker basado en la ultima version de Ubuntu-Linux
    La estructura de la aplicación es la siguiente:
    
        /Instance
        /src
            /Blueprints             # Blueprints de los endpoints
            /Calculations           # Metodos para calcular remanentes, rendimientos etc.
            /CoreLogic              # Metodos que mandan el flujo de aplicacion
            /DataManipulation       # Manipulacion de datos, union de listas etc.
            /DataModels             # Modelos de respuestas y datos
            /DB                     # Manejador de la base de datos
            __init__.py             # Application Factory
            schema.sql              # esquema de la base de datos
            DockerFile              # Creacion de la imagen del contenedor docker


Implementacion:


Generar la imagen Docker con el siguiente commando: (se instalan las dependencias necesarias al generar el contenedor)

    docker build -t blk-hacking-mx-leonardo-lameda .

Correr el contenedor:

    docker run -d -it --name blk-hacking-mx-leonardo-lameda -p 5477:80 blk-hacking-mx-leonardo-lameda

Activar el ambiente virutal de Python

    . .venv/bin/activate

Arrancar la base de datos:

    python3 -m flask --app src init-db

Iniciar la aplicacion:

    python3 -m flask --app src run --port 80


