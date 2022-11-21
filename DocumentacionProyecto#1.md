# **Documentación del Proyecto#1**

## **Instalación**

Primero debera de tener instalado las siguientes aplicaciones:
1. Docker desktop con kubernetes habilitado
2. Minikube
3. Helm
4. Powershell
5. Lens

**Importante**  

Se debe clonar el repo de github: https://github.com/notthatdood/DataMigrationPlatform.
Luego se abre powershell y se hace un change directory a donde se haya colocado el repositorio.

#### Instalar las herramientas principales

1. Abrir el powershell y buscar el repositorio del proyecto

2. Ejecutar el script llamado "createBase.ps1"

```sh
./createBase.ps1
``` 
[![Captura.png](https://i.postimg.cc/vTgHB5Xz/Captura.png)](https://postimg.cc/WqVPYFBF)

Esperar a que esten arriba todos los pods

1. Hacer el port forward de mariadb
```sh
kubectl port-forward --namespace default svc/databases-mariadb 3306:3306
``` 
[![Captura2.png](https://i.postimg.cc/yNpMdxx6/Captura2.png)](https://postimg.cc/FfcWC90w)

1. Correr el script populateMariaDB.py

```sh
python ./scripts/pythonScripts/FillDBs/populateMariaDB.py
``` 
6. Correr el script para crear los deployments de python
```sh
./createDMP.ps1
``` 

7. Hacer el port forward de elasticsearch
```sh
kubectl port-forward --namespace default svc/databases-elasticsearch 9200:9200
``` 
[![Captura3.png](https://i.postimg.cc/nz6N4Wq6/Captura3.png)](https://postimg.cc/hz1Cgpyr)


1. Correr el script para insertar un job nuevo(inmediatamente corrido este debemos cerrar el port forward de elastic)

```sh
insertJob.py
``` 

9. Para ver el resultado en el índice persona corra el siguiente script "viewElastic.py" (Se encuentra enla carpeta: DataMigrationPlatform\scripts\pythonScripts\)
    


## **Conclusiones/Recomendaciones**  

 * Como recomendación, para importar un dashboard se debe crear primero el data sources de prometheus. Esto se debe a que en el dashboard hay indicarle prometheus como data source.
 * Tener todo instalado (helm, minikube, etc) ya que todo es importante y primordial.
 * Buscar las imagen de python en linux fue bastante complicado ya que no funcionaban las imagenes de MariaDB. Sin embargo se solucionó seleccionando una versión específica de mariaDB e importando una librería adicional.

## **Referencias Bibliograficas**

* RabbitMQ tutorial - «Hello world!» — RabbitMQ. (s. f.). Recuperado 21 de octubre de 2022, de https://www.rabbitmq.com/tutorials/tutorial-one-python.html
* Python Elasticsearch Client — Python Elasticsearch client 8.4.3 documentation. (s. f.). Recuperado 21 de octubre de 2022, de https://elasticsearch-py.readthedocs.io/en/v8.4.3/
