#Pre-requisites
#tener docker desktop con kubernetes habilitado
#tener un instalation de minikube, usamos el 1.25
#(minikube ya trae kubectl entonces no lo incluimos)  
#instalar helm





#Primero clonar el repo de github, entrar al directorio en el que se encuentra el repo

#Inicializar minikube
minikube start

#Para crear las dependencias y agregar el repo
helm repo add bitnami https://charts.bitnami.com/bitnami
helm dependency build databases
helm dependency build monitoring
helm dependency update databases
helm dependency update monitoring

#importante primero instalar el de monitoring para que se cree la definición del serviceMonitor
helm install monitoring monitoring
helm install databases databases --render-subchart-notes

#port forwarding de ES y Kibana
#TODO: revisar el comando curl
#kubectl port-forward --namespace default svc/databases-elasticsearch 9200:9200
#nosequehaceestocurl http://127.0.0.1:9200/
#kubectl port-forward svc/databases-kibana 8080:5601
#para ver el estado de los pods puede ser en lens o con este comando
#kubectl get pods

#para ver releases instalados
#helm list

#para desinstalar 
#helm delete "releaseName"

#para borrar minikube
#minikube delete minikube