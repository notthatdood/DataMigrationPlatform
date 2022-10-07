#Pre-requisites
#tener docker desktop con kubernetes habilitado
#tener un instalation de minikube, usamos el 1.25
#(minikube ya trae kubectl entonces no lo incluimos)  
#instalar helm





#Primero clonar el repo de github, entrar al directorio en el que se encuentra el repo

#Inicializar minikube
minikube start --cpus 4

#Para crear las dependencias y agregar el repo
helm repo add bitnami https://charts.bitnami.com/bitnami

helm dependency build monitoring
helm dependency build databases
helm dependency build components

helm dependency update monitoring
helm dependency update databases
helm dependency update components


#importante primero instalar el de monitoring para que se cree la definición del serviceMonitor
helm install monitoring monitoring
helm install databases databases #--render-subchart-notes
helm install components components



#helm install kibana bitnami/kibana --set elasticsearch.hosts[0]=localhost --set elasticsearch.port=9200


#port forwarding de ES y rabbitmq
#TODO: revisar el comando curl
#kubectl port-forward --namespace default svc/databases-elasticsearch 9200:9200
#kubectl port-forward --namespace default svc/components-rabbitmq 5672:5672

#para ver el estado de los pods puede ser en lens o con este comando
#kubectl get pods

#pasarle host y puerto a kibana
#helm upgrade --namespace default databases bitnami/kibana --set elasticsearch.hosts[0]="localhost",elasticsearch.port="9200"

#para ver releases instalados
#helm list

#para desinstalar 
#helm delete "releaseName"

#para borrar minikube
#minikube delete minikube