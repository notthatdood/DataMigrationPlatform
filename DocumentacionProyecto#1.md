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
1. Lo primero que tienen que hacer es tener instalado el powerShell, luego correr las dependencias para instalar.

```sh
pip install pika
pip install elasticsearch
pip install mysql
pip install mariadb
pip install prometheus-client
```  
2. Abrir el powershell y buscar el repositorio del proyecto

3. Ejecutar el script llamado "createEverything.ps1"

```sh
./createEverything.ps1
``` 
[![Captura.png](https://i.postimg.cc/vTgHB5Xz/Captura.png)](https://postimg.cc/WqVPYFBF)

4. Dentro del powershell correr los forwards de mariadb, elastic y rabbitmq (hacerlo uno en cada ventana para cortar tiempo)

```sh
kubectl port-forward --namespace default svc/components-rabbitmq 5672:5672
``` 
[![Captura1.png](https://i.postimg.cc/RFyxPhxp/Captura1.png)](https://postimg.cc/MM7LHWT1)

```sh
kubectl port-forward --namespace default svc/databases-mariadb 3306:3306
``` 
[![Captura2.png](https://i.postimg.cc/yNpMdxx6/Captura2.png)](https://postimg.cc/FfcWC90w)

```sh
kubectl port-forward --namespace default svc/databases-elasticsearch 9200:9200
``` 
[![Captura3.png](https://i.postimg.cc/nz6N4Wq6/Captura3.png)](https://postimg.cc/hz1Cgpyr)

5. Entrar al scripts/pythonScripts/fillDBs y correr script:

```sh
populateMariaDB.py
``` 

 Y luego correr el siguiente script en lla misma carpeta:

```sh
insertJob.py
``` 
6. Abrir cualquier navegador y pones el link (http://localhost:8000/) para revisar las metricas del prometheus.

7. Despues se van a correr los scripts que van a estar en los pods de python en el powerShell. Esto se encuentra en la carpeta "DataMigrationPlatform\scripts\pythonScripts\deploymentLogic"

 Se deben correr en el siguiente orden: 
    1. orchestratorLogic.py
    2. MySQLConnectorLogic.py
    3. SQLProcessorLogic.py
    4. RegexProcessor.py
    5. ElasticsearchPublisherLogic.py

8. Para ver el resultado en el índice persona corra el siguiente script "viewElastic.py" (Se encuentra enla carpeta: DataMigrationPlatform\scripts\pythonScripts\)
    

## **Creacion de imagenes Docker y Deployments en Kubernetes**

1. Navegar al directorio /consumer-producer de cada uno de los cinco componentes (Orchestrator por ejemplo)
2. Esto es todo lo necesario para crear el deployment en Kubernetes.
3. Se hace docker pull del repositorio israelhercam en el que las imágenes de cada deployment ya están subidas.

    docker pull israelhercam/orchestrator-image
    kubectl apply -f consumer-producer.yaml

4. Para crear la imagen de cada component y subirla a un repositorio, se necesaitan los siguientes pasos.
5 .Navegar al directorio /consumer-producer de cada uno de los cinco componentes (Orchestrator por ejemplo).
```sh
    sudo docker login
    sudo docker build -t [reponame]/[image-name] .
    sudo docker images
    sudo docker push [reponame]/[image-name]
    kubectl apply -f consumer-producer.yaml
```
6. Eliminar el deployment creado
```sh
    kubectl delete -f consumer-producer.yaml
```
## **Conclusiones/Recomendaciones**  

 * Como recomendación, para importar un dashboard se debe crear primero el data sources de prometheus. Esto se debe a que en el dashboard hay indicarle prometheus como data source.
 * Tener todo instalado (helm, minikube, etc) ya que todo es importante y primordial.
 * Buscar las imagen de python en linux fue bastantes complicado ya que no funcionaban las imagenes de MariaDB.

## **Referencias Bibliograficas**

* RabbitMQ tutorial - «Hello world!» — RabbitMQ. (s. f.). Recuperado 21 de octubre de 2022, de https://www.rabbitmq.com/tutorials/tutorial-one-python.html
* Python Elasticsearch Client — Python Elasticsearch client 8.4.3 documentation. (s. f.). Recuperado 21 de octubre de 2022, de https://elasticsearch-py.readthedocs.io/en/v8.4.3/
