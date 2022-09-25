# **Documentación de la tarea 1**

## **Instalación**

  
Antes de ejecutar cualquier comando se debe tener instalado en el equipo:
1. Docker desktop con kubernetes habilitado
2. Helm
3. Minikube
4. Powershell

**Con Minikube**  

Se debe clonar el repo de github: https://github.com/notthatdood/TareaCorta1.
Luego se abre powershell y se hace un change directory a donde se haya colocado este repo.

#### Instalar las herramientas de monitoreo y bases de datos
En la configuración de este helm chart solo están habilitadas prometheus y grafana, thanos está deshabilitada para su instalación. Solo se debe configurar el values.yaml de la carpeta monitoring para habilitarlo. Más adelante ejemplifica.  

1.Desde línea de comandos en Windows se debe ejecutar:
```sh
./createEverything.ps1
```  
**Sin Minikube**  

1.Desde línea de comandos se debe ejecutar:
```sh
helm install monitoring monitoring --dependency-build
```  
2.Luego descargar todas las dependencias de las herramientas a utilizar
```sh
helm install monitoring monitoring --dry-run
```  
2.Actualizamos las dependencias:  
```sh
helm install database database --dependency-build
```  
3.Para instalar las bases de datos se debe ejecutar el siguiente comando:  
```sh
helm install database database --dry-run
```
## **Configuración de grafana**

Luego de tener instaladas las bases que vamos a utilizar y las herramientas que van a monitorear esa base de datos. Podemos ingresar a grafana.  

1.Nos vamos a la línea de comandos y ejecutamos lo siguiente:
```sh
 kubectl port-forward svc/monitoring-grafana 8080:3000
```  
  
2.Entramos al navegador e ingresamos a grafana utilizando la dirección:  

http://127.0.0.1:8080

3.Escribimos las credenciales, por defecto será el usuario "admin" y la contraseña será "tarea1", esta contraseña está configurada en el values.yaml del helm chart "monitoring".

![N|Solid](https://i.pinimg.com/564x/59/67/f5/5967f5e69af4fd8c478b30827091462a.jpg)  

4.Nos vamos a la parte de configuración y Data sources  

![N|Solid](https://i.pinimg.com/originals/68/c9/f3/68c9f3724b86c67ea6858e56d9ebf2d2.jpg)  

5.Añadimos el data souces y seguidamente prometheus 

![N|Solid](https://i.pinimg.com/originals/ed/bb/a7/edbba713ff4d5a96e3bf25258d59cb68.jpg)  

![N|Solid](https://i.pinimg.com/originals/04/bc/e6/04bce615e432a85d4e588fe5bf958ebc.jpg)  

5.Indicamos el url de prometheus el cual será: http://monitoring-kube-prometheus-prometheus:9090  y guardamos los cambios. Debe aparecer un mensaje en donde indique que el Data source está funcionando.

![N|Solid](https://i.pinimg.com/originals/81/aa/d7/81aad70ee0eaf0518108d06a3712dbf6.jpg)  
![N|Solid](https://i.pinimg.com/originals/ee/5a/ef/ee5aefb88578c083f766c07441381145.jpg)  

**Añadiendo los dashboard de las bases de datos**  
  
Nos vamos a la pestaña de general de grafana e importamos un dashboard. Se ejecuta la misma acción cuando se desee añadir uno nuevo.  

![N|Solid](https://i.pinimg.com/originals/b4/4d/3d/b44d3dc006c9993d9d1eb4ec2872aa48.jpg)  

**MariaDB**  

Dashboard con el ID 13106.  

![N|Solid](https://i.pinimg.com/originals/b0/cb/e6/b0cbe6abc78b767ce2433ac20562d5ba.jpg)
  
**MongoDB**  

Dashboard con el ID 2583.  

![N|Solid](https://i.pinimg.com/originals/21/e5/5d/21e55d678eff510fb90fe275a6fd2a0e.jpg)
  
**Elasticsearch**  

Dashboard con el ID 2322.  

![Screenshot](https://i.pinimg.com/originals/f6/ab/21/f6ab215a41d38dd6554a3ed3ac1e7857.jpg) 
  
**PostgreSQL**  

Dashboard con el ID 9628.  

![N|Solid](https://i.pinimg.com/originals/e8/33/b3/e833b391b4db639ac3297eab44d5107c.jpg)


## **Configuración de las herramientas**  

**MariaDB**  

Añadimos el user y password para abrir y que funciones MariaDB y habilitamos el service monitor para las métricas.

[![maria-DBconfiguration.png](https://i.postimg.cc/SsFfgxVC/maria-DBconfiguration.png)](https://postimg.cc/7C9z6DFZ)
  
**MongoDB**  

Añadimos el user y password para abrir y que funciones MongoDB y habilitamos el service monitor para las métricas.

[![mongo-DBconfiguration.png](https://i.postimg.cc/mDYNJW6q/mongo-DBconfiguration.png)](https://postimg.cc/N90H2St7)
  
**Elasticsearch**  

Se deben de añadir nodos (minimo un nodo) en el area de master y se tiene que crear 3 replicas como minimo para que pueda funcionar Elasticsearch.
Habilitamos el service monitor para las métricas.

[![db3.png](https://i.postimg.cc/3wDZjvj3/db3.png)](https://postimg.cc/nsp7pMwW)
  
**PostgreSQL**  

Añadimos el user y password para abrir postgresql y habilitamos el service monitor para las métricas.

![N|Solid](https://i.pinimg.com/originals/64/e7/34/64e7341ee9bf014d6b53b067e614c6d2.jpg)
  
## **Pruebas de Gatling**

Para realizar las pruebas en Gatling se intentó inicialmente utilizar Flask como intermediario entre las bases de datos y Gatling. Se siguió la guía de la documentación del sitio web oficial de Flask (Flask, 2010) para montar la aplicación de Flask. Se logró montar la aplicación de Flask con normalidad y siguiendo la guía fue muy sencillo, sin embargo no se logró conectar con Gatling para hacer las pruebas de rendimiento a las bases de datos.

Al no poder utilizar Flask como parte de la implementación de gatling se intentó usar Gatling directamente descargando el Gatling Bundle de su página oficial. Se siguió la guía del video publicado por Automatation Step By Step (Pal, 2022).
Antes de empezar al proyecto de Gatling se necesita lo siguiente:

- Tener instalado el JDK.
- Descargar el Gatling Bundle
- Instalar el lenguaje de programación Scala.
- Descargar Maven para crear el proyecto.

A la hora de realizar pruebas de gatling por si solo, se utilizó el sitio web demo de Orange HRM (https://opensource-demo.orangehrmlive.com/web/index.php/auth/login). Al estar dentro de este sitio web, se presiona F12 y se va a la sección que dice "Red". En la sección de Red se presiona el botón de grabar y se comienzan a ingresar datos en la página demo.
Después de grabar las acciones, se seleccióna la opción de guardar los datos como un archivo .HAR y este se ingresa a la interfaz que se despliega al correr el archivo recorder.bat del Gatling Bundle. Al ingresar el archivo gatling genera un link en el que se pueden observar los gráficos de las pruebas realizadas, además de crear un script para correr las pruebas el cual se puede editar también para alterar la cantidad de usuarios que "ingresarían a la base" en la simulación de Gatling.

La prueba con el sitio web demo y sin conecciones se realizaron con éxito, sin embargo no se logró enlazar Gatling directamente con los pods de las bases de datos.
 
## **Conclusiones**  

La Tarea fue bastante interesante para aprender y saber configurar e intalar los tipos base de datos SQL y NoSQL mediante kubernetes. Fue interesante aprender instalar el docker desktop, helm, minikube y poder activar los kubernetes, aunque todo fue instalacion y seguir los pasos fue una leccion para otros proyectos. Al igual fue con las instalacion de Prometheus y Grafana, ninguno esperaba que fuera complicado hacer las configuraciones para que las app funcionaran y es algo que el equipo aprendio.
Fue interesante hacer los benchmarks para cada tipo de base de datos SQL y NoSQL y se aprendio que para cada base de datos mediante kubernetes se tiene que modelar dirente para que pueda funcionar.
  
## **Recomendaciones**  

* Como recomendación, para importar un dashboard se debe crear primero el data sources de prometheus. Esto se debe a que en el dashboard hay indicarle prometheus como data source.  

* Como segunda recomendación, es ideal que se habiliten solo las bases de datos que se vayan a utilizar para que no consuma muchos recursos y que corra más rápido.

* Otra recomendacion seria, lo mas accesible y comodo para trabajar es configurar la terminal de linux dentro del PowerShell como extension, aunque se puede trabajar desde la misma terminal de ubuntu a la hora de correr comandos y scripts es mas agradable trabajarlo todo desde el PowerShell ademas la terminal de ubuntu tiene algunos fallos y no te deja correrlo.

## **Referencias**

Flask, . (2010). Application setup. Application Setup - Flask Documentation (2.2.x). Retrieved September 18, 2022, from https://flask.palletsprojects.com/en/2.2.x/tutorial/factory/

YouTube. (2022). Gatling Beginner Tutorial 1 | Load Testing, Introduction, Download, Setup |. YouTube. Retrieved September 16, 2022, from https://www.youtube.com/watch?v=CPBWawzVeTo&amp;t=6s. 

Loewen, C. (2022, 12 agosto). Advanced settings configuration in WSL. Microsoft Learn. Recuperado 18 de septiembre de 2022, de 
https://learn.microsoft.com/en-us/windows/wsl/wsl-config#configure-global-options-with-wslconfig
