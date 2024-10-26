# POSTGRES-CHROMADB-COMPARISON

## Postgresql

### Local install windows

Installation in windows by using the installer found on the website [link](https://www.postgresql.org/download/)

If you want to use the postgres command you should add to your PATH (environmental variable) the folder of the installation of psql. Add in this case the bin folder that contains all the utility that you can use for managing the server.
On top of that postgres installation provide a frontend in which you can perform different type of queries operation and visualize you data.

After the installation in windows in order to start it use this command:
pg_ctl.exe restart -D "C:\Program Files\PostgreSQL\17\data"
This will start the server and you can create connection and exchange messages between client and server.

### Docker install

Install docker or docker desktop
Follow this command to get the image
docker pull postgres:16
For starting the server in a vm using docker:
docker run --name test-vector-db -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:16

(you can also place the vm in a separated network)

**_NOTA: the 17 version of postgresql doesnt support the vector extension. In order to use it you need to downgrade to PG 16 at least_**

In order to create a conda environment run:
conda create -n vecdb-test
To activate it:
conda activate vecdb-test

## Libraries

in requirements.txt

## Conf postgres

user: postgres
pass: postgres

## Convert from normal postgres database to pgvector

I inserted fake data in order to see if anything changes if I need to apply this modification. The fake data can be found [here](./fake_data.sql).
I want to introduce this guide in order to add the functionality of storing embeddings in an already functioning postgres database. This doesn't come as activated by default but you need to activate it by yourself (unless you install from scratch or use the docker image provided).
In order to transform your db the following steps are required:

1. go inside exec and run apt update
2. install pgvector with the following command: apt install postgresql-16-pgvector (change the version accordingly)
3. run through sql: CREATE EXTENSION vector;

Table create like this:
CREATE TABLE items (id bigserial PRIMARY KEY, content TEXT, embedding vector(384));

## DA RISOLVERE

- [ ] Perchè non si vedono i vettori una volta  runnato lo script?

## TEST PGVECTOR CON PG17

## PROVARE A DOCKERIZZARE L'APP PER FAR PRATICA CON IL DOOCKERFILE
