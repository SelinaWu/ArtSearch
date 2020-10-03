# ArtSearch
Develop a full-functioning art search engine.


### Implement 2 basic features:
1) receive file name and return the file
2) receive an image and find the most similar image and return

### Add 3 additional features:
3) Feature 1 MongoDB/MySQL/any database + stateful set (Selina)
4) Feature 5 New metric (Alice, Javin)
5) Feature 8 Aesthetically pleasing frontend(s) (Lin)

### Relevant Doc
[Google Doc](https://docs.google.com/document/d/1wCjr7nEeb-J4IZ7t8HJxeMzG3G4R0kNWznpK6ybn7o0/edit)

### gcp MySQL 

instance_id: artimages
<br>
root password: ArtSearchAm295

Current method: 
[Connect Cloud SQL to Python - pymysql](https://cloud.google.com/sql/docs/mysql/connect-external-app#pymysql-tcp)
- Install Proxy on Mac: <br>
`curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64`<br>
`chmod +x cloud_sql_proxy`<br>
- Start Proxy in cmd:`./cloud_sql_proxy -instances=ac295-data-science-289013:us-east1:artimages=tcp:3306`<br>
Note: `ac295-data-science-289013:us-east1:artimages` is Selina's sql instance <br>
- In python: `python sql_test.py`
- Load csv to sql server in python: [link](https://datatofish.com/import-csv-sql-server-python/)


Previous method (ignore):
[instruction](https://cloud.google.com/sql/docs/sqlserver/quickstart)
Exist error from SSMS.

