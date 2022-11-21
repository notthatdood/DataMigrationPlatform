#code from https://www.rabbitmq.com/tutorials/tutorial-one-python.html
#Code from: https://elasticsearch-py.readthedocs.io/en/v8.4.3/
#!/usr/bin/env python
import json 
from elasticsearch import Elasticsearch
#Escuchar db de elasticSearch
es = Elasticsearch(hosts="https://localhost:9200", basic_auth=("elastic","password"), verify_certs=False)

doc= {
    "job_id": "job606",
    "status": "new",
    "msg": "",
    "data_sources": [
        {
            "type": "mysql",
            "name": "people_db",
            "url": "databases-mariadb-people",
            "port": "3306",
            "usuario": "XXXXXXX",
            "password": "XXXXXXX"
        },
        {
            "type": "mysql",
            "name": "car_db",
            "url": "databases-mariadb-people",
            "port": "3306",
            "usuario": "XXXXXX",
            "password": "XXXXXX"
        },
        {
            "type": "elasticsearch",
            "name": "destination_es",
            "url": "https://quickstart-es-http",
            "port": "9200",
            "usuario": "XXXXXXXXXX",
            "password": "XXXXXXXXX"
        }
    ],
    "control_data_source": "destination_es",
    "source": {
        "data_source": "people_db",
        "expression": "SELECT * FROM persona ORDER BY cedula",
        "grp_size": "100"
    },
    "stages" : [
        {
            "name": "extract",
            "source_queue": "extract",
            "destination_queue": "%{transform->transformation->add_car}%"
        },
        {
            "name": "transform",
            "transformation": [
                {
                    "name": "add_car",
                    "type": "sql_transform",
                    "table": "car",
                    "expression": "SELECT %{field_description}% FROM %{table}% WHERE %{field_owner}% = %{doc_field}%",
                    "source_data_source": "car_db",
                    "destination_data_source": "destination_es",
                    "doc_field": "id",
                    "source_queue": "sql_queue",
                    "destination_queue": "%{transform->transformation->myregex}%",
                    "fields_mapping": {
                        "field_description": "description",
                        "field_owner": "owner"
                    }
                },
                {
                    "name": "myregex",
                    "type": "regex_transform",
                    "regex_config": {
                        "regex_expression": "^.* ([a-zA-z]{3}-[0-9]{3}) .*$",
                        "group": "1",
                        "field": "description"
                    },
                    "field_name": "placa",
                    "source_queue": "regex_queue",
                    "destination_queue": "%{load}%"
                }
            ]
        },
        {
            "name": "load",
            "source_queue": "ready",
            "destination_data_source": "destination_es",
            "index_name": "persona"
        }
    ]
}

resp = es.index(index="jobs",id=1, document=doc)
print(resp['result'])




