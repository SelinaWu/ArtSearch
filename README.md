# ArtSearch
Develop a full-functioning art search engine.


### Implement 2 basic features:
1) receive file name and return the file
2) receive an image and find the most similar image and return

### Add 3 additional features:
3) Feature 1 MongoDB/MySQL/any database + stateful set (Selina)
4) Feature 5 New metric (Alice, Javin)
5) Feature 8 Aesthetically pleasing frontend(s) (Lin)

### Docker
-Create a container for image display (port 8081):
`docker build -t task2:frontend -f Docker_filename_frontend .`<br>

-Create a container for image Search (Cosine Similarity) (port 8083):
`docker build -t task1:frontend -f Docker_image_frontend  .`<br>

-Create a container for database deployment (port 8082):
`docker build -t webapp:db -f Docker_maindb .`<br>

### KUBERNETES COMMANDS
After we configure our YAML file, we did our following steps: <br>

Testing local deployment on minikube
`Minikube start`

--Deploy configmap: <br>
`kubectl apply -f webapp_configmap.yml`

--Deploy database: <br>
`kubectl apply -f web_db_deployment.yml`

--Deploy image search front end: <br>
`kubectl apply -f image_deploy_k8s.yml`


### GCP Deployment COMMANDS

We create our cloud project as : ac295artsearch <br>

`export PROJECT_ID = ac295artsearch` <br>

--retagging our container images <br>
`docker image tag 2aaed1f70b81 gcr.io/${PROJECT_ID}/task1:frontend` <br>
`docker image tag 8c85bd87bdd0 gcr.io/${PROJECT_ID}/webapp:db ` <br>
`docker image tag 83c87d0db087 gcr.io/${PROJECT_ID}/task2:frontend `<br>


--Push containers to cloud<br>
`docker push gcr.io/${PROJECT_ID}/webapp:db` <br>
`docker push gcr.io/${PROJECT_ID}/task1:frontend` <br>
`docker push gcr.io/${PROJECT_ID}/task2:frontend `<br>



--Create Cluster and deploy<br>
`gcloud container clusters create artsearch-cluster --num-nodes 3` <br>
`kubectl apply -f webapp_configmap.yml` <br>
`kubectl apply -f web_db_gcp.yml` <br>
`kubectl apply -f image_deploy_gcp.yml` <br>




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


Previous method (ignore):
[instruction](https://cloud.google.com/sql/docs/sqlserver/quickstart)
Exist error from SSMS.

