#minikube start
#helm repo add elastic https://helm.elastic.co
##helm dependency build dbTest
#helm install elastic-operator elastic/eck-operator -n elastic-system --create-namespace
#helm install elastic-stack ./stack


minikube start

# Add the Elastic Helm Repository
helm repo add elastic https://helm.elastic.co && helm repo update

# Install the ECK Operator cluster-wide
helm install elastic-operator elastic/eck-operator -n elastic-system --create-namespace

# Install the ECK-Stack helm chart
# This will setup a 'quickstart' Elasticsearch and Kibana resource
helm install testdb -n default elastic/eck-stack --create-namespace