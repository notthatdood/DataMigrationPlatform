# **Documentación de la tarea 1**

## **Instalación**

  
Antes de ejecutar cualquier comando se debe tener instalado en el equipo:
1. Docker desktop con kubernetes habilitado
2. Helm
3. Minikube
4. Powershell

**Con Minikube**  

Se debe clonar el repo de github: https://github.com/notthatdood/DataMigrationPlatform.
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
## **Configuración de ElasticSearch**
1. En la línea de comandos escribimos el siguiente:
```sh
kubectl port-forward --namespace default svc/databases-elasticsearch 9200:9200
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
  
  
**Elasticsearch**  

Dashboard con el ID 2322.  

![Screenshot](https://i.pinimg.com/originals/f6/ab/21/f6ab215a41d38dd6554a3ed3ac1e7857.jpg) 

## **Configuración de las herramientas**  

**MariaDB**  

Añadimos el user y password para abrir y que funciones MariaDB y habilitamos el service monitor para las métricas.

[![maria-DBconfiguration.png](https://i.postimg.cc/SsFfgxVC/maria-DBconfiguration.png)](https://postimg.cc/7C9z6DFZ)
  
  
**Elasticsearch**  

Se deben de añadir nodos (minimo un nodo) en el area de master y se tiene que crear 3 replicas como minimo para que pueda funcionar Elasticsearch.
Habilitamos el service monitor para las métricas.

[![db3.png](https://i.postimg.cc/3wDZjvj3/db3.png)](https://postimg.cc/nsp7pMwW)
  
  

## **Conclusiones**  

La Tarea fue bastante interesante para aprender y saber configurar e intalar los tipos base de datos SQL y NoSQL mediante kubernetes. Fue interesante aprender instalar el docker desktop, helm, minikube y poder activar los kubernetes, aunque todo fue instalacion y seguir los pasos fue una leccion para otros proyectos. Al igual fue con las instalacion de Prometheus y Grafana, ninguno esperaba que fuera complicado hacer las configuraciones para que las app funcionaran y es algo que el equipo aprendio.
Fue interesante hacer los benchmarks para cada tipo de base de datos SQL y NoSQL y se aprendio que para cada base de datos mediante kubernetes se tiene que modelar dirente para que pueda funcionar.
  
## **Recomendaciones**  

* Como recomendación, para importar un dashboard se debe crear primero el data sources de prometheus. Esto se debe a que en el dashboard hay indicarle prometheus como data source.  

* Como segunda recomendación, es ideal que se habiliten solo las bases de datos que se vayan a utilizar para que no consuma muchos recursos y que corra más rápido.

* Otra recomendacion seria, lo mas accesible y comodo para trabajar es configurar la terminal de linux dentro del PowerShell como extension, aunque se puede trabajar desde la misma terminal de ubuntu a la hora de correr comandos y scripts es mas agradable trabajarlo todo desde el PowerShell ademas la terminal de ubuntu tiene algunos fallos y no te deja correrlo.

## **Referencias**


