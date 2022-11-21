#update es publisher
Set-Location images/elasticsearch-publisher
docker build -t notthatdude/elasticsearch-publisher .
docker push notthatdude/elasticsearch-publisher
Set-Location ..
Set-Location ..

#update mysql connector
Set-Location images/mysql-connector
docker build -t notthatdude/mysql-connector .
docker push notthatdude/mysql-connector
Set-Location ..
Set-Location ..

#update orchestrator
Set-Location images/orchestrator
docker build -t notthatdude/orchestrator .
docker push notthatdude/orchestrator
Set-Location ..
Set-Location ..

#update regex-processor
Set-Location images/regex-processor
docker build -t notthatdude/regex-processor .
docker push notthatdude/regex-processor
Set-Location ..
Set-Location ..

#update sql-processor
Set-Location images/sql-processor
docker build -t notthatdude/sql-processor .
docker push notthatdude/sql-processor
Set-Location ..
Set-Location ..