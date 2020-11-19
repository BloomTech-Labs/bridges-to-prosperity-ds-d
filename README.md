# Welcome to our Repo! 
[![Welcome Video](https://imgur.com/7gaai5K.png)](https://youtu.be/1qVVODfPtto)

# Links to Deployments
<p>&nbsp;</p>

[Docs](https://docs.labs.lambdaschool.com/data-science/)

[Latest deployment](https://lab28dsk.bridgestoprosperity.dev/)

[Previous deployment](https://b2pmergefinal.bridgestoprosperity.dev/)

[Deployed API](https://d-ds.bridgestoprosperity.dev/) 

[Deployed API#2](https://d-ds-labs28.bridgestoprosperity.dev )

# Architeture

https://github.com/Lambda-School-Labs/bridges-to-prosperity-ds-d/blob/main/assets/Screen%20Shot%202020-11-19%20at%208.18.23%20AM.png

# How to Create DataBase Hosted in AWS 
- Log In w/ Credentials to AWS
- Relational DataBase Section
- Click Create DataBase, choose desired database, ex) PostGres
- Configure Settings, Make Password, Username
- Connect with pgadmin, datagrip
- TIP: Allow public access, create security groups incase you have trouble connecting via your domain

# How to Connect to data Base
- Save secret in .env file into 
- Create connection, cursor to the database using psycopg2
- Can make a function that constructs connections via function or simply type connections explicitly
```python
    def conn_curs():
        """
        makes a connection to the database
        """
        global db_name
        global db_user
        global db_password
        global db_host
        global db_port
        
        connection = psycopg2.connect(dbname=db_name, user= db_user,
                                      password=db_password, host= db_host,port=db_port)
        cursor = connection.cursor()
        return connection, cursor
```
# How to upload Data Frame as SQL Table to DataBase
- Convert CSV/Excel into DataFrame format : 
```python 
   #Make sure your file location does actually coresspond to a  working link
   df = pd.read("file_location")
```
- Upload DataFrame to SQL Table
```python   
   table_name = 'table_name'
   df.to_sql(table_name, con)
```
- Test SQL Table that is connected to DataBase.
- Check out Bridges_2_Prosperity_Final_Merged_DataFrameToPostgresSQL.ipynb notebook to see an example.

## Test Queries to Table B2P_oct_2018

```python
    
    # Testing Query to get Records based on Bridge Naem
    conn, cursor = conn_curs()
    query  = """SELECT "Bridge_Name" from public."B2P_oct_2018" where "Bridge_Name" = 'Bukinga' LIMIT 1;"""
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close
```

# How to Run App Locally
- Make sure u have a local.env file with proper secrets
- Save your .env file in the following location: project/app/api/.env 
- Go to your terminal run: docker-compose up






