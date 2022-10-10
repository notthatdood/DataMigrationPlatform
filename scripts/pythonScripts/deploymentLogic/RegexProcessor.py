from elasticsearch import Elasticsearch
import re


es = Elasticsearch(hosts="https://localhost:9200", http_auth=("elastic","password"),verify_certs=False)

resp = es.get(index="jobs", id=1)
print(resp['_source'])

es.indices.refresh(index="jobs")

resp = es.search(index="jobs", query={"match_all": {}})

#Regular expression match logic
txt = "Toyota Corollacross BWC-166, Blanco Perlado"
txt1 = "Honda CRV HUJ-987, Dorado"

#Returns a list with the match
#Parameters need to be replaced by the ones provided on the job file.
x = re.findall("^.*([a-zA-z]{3}-[0-9]{3}).*$", txt)
x1 = re.findall("^.*([a-zA-z]{3}-[0-9]{3}).*$", txt1)
print(x,x1)

#Falta de terminar, lógica de reemplazo es la misma que la de SQL Processor