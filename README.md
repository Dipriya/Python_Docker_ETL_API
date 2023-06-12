# Python_Docker_ETL_API

Below are the sequence of steps followed to build, run and trigger ETL process of my application. 

Installed Applications: Docker Destop 4.20.1, Python 3.11 (latest), PostgreSql 15.3

**Step 1:**
 
 Using CommandLine (CMD) on Windows 10, 
     
   **Step 1.1** Created Project directory and sub-directory for the project.
        
        mkdir python-docker-ETL
        
        mkdir etl-pipeline
          
  **Step 1.2** Setup Virtual Environments (venv) - It is lightweight virtual environment which has its own Python binary 
and set of installed Python packages.
        
      python -m venv venv     # Creates the Virtual environment.
      
      venv\Scripts\activate.bat     # Activates the Virtual environment.
      
   **Step 1.3** Installed all the applications needed in the Virtual environment (venv)
      
      pip3.11 install Flask      # Installed Flask-2.3.2 Jinja2-3.1.2 MarkupSafe-2.1.3 Werkzeug-2.3.6 blinker-1.6.2 click-8.1.3 colorama-0.4.6 itsdangerous-2.1.2
      
      pip3.11 install pandas     # Installed numpy-1.24.3 pandas-2.0.2 python-dateutil-2.8.2 pytz-2023.3 six-1.16.0 tzdata-2023.3
      
      pip3.11 install psycopg2   # Installed psycopg2-2.9.6 for Postgres Connection
   
**Step 2:**
  
  Build the Docker image from Terminal (CMD) in the Virtual environment (venv). 
  
  Find attached Dockerfile, requirements.txt and app.py code that is used to build the docker image.
      
      docker build -t etlapp:v1 .

  Here is the snip of the build,

    (venv) .\etl-pipeline>docker build -t etlapp:v1 .

    [+] Building 63.2s (11/11) FINISHED

     => [internal] load .dockerignore                                                                                  0.1s

     => => transferring context: 2B                                                                                    0.0s

     => [internal] load build definition from Dockerfile                                                               0.1s

     => => transferring dockerfile: 227B                                                                               0.0s

     => [internal] load metadata for docker.io/library/python:latest                                                   1.8s

     => [internal] load build context                                                                                  0.0s

     => => transferring context: 126B                                                                                  0.0s

     => [1/6] FROM docker.io/library/python:latest@sha256:380d708853b1564b71ad3744a69895d552099f618df60741c5d4a9e9e65  0.1s

     => => resolve docker.io/library/python:latest@sha256:380d708853b1564b71ad3744a69895d552099f618df60741c5d4a9e9e65  0.1s

     => CACHED [2/6] WORKDIR /etlcode                                                                                  0.0s

     => [3/6] COPY requirements.txt .                                                                                  0.1s

     => [4/6] RUN pip3.11 install -r requirements.txt                                                                 56.2s

     => [5/6] COPY src/ .                                                                                              0.1s

     => [6/6] COPY requirements.txt /etlcode                                                                           0.1s

     => exporting to image                                                                                             4.4s

     => => exporting layers                                                                                            4.4s

     => => writing image sha256:a3ccb44e3dc2ac849cc654e99bbac9bd7274f637098d1d82d9d722cdd1153300                       0.0s

     => => naming to docker.io/library/etlapp:v1

**Step 3:** 

Run the Docker container, print container ID and publish the container's port to the host from Terminal (CMD) in the Virtual 
environment (venv)

    docker run --name dipriya_pillai -d -p 5000:5000 etlapp:v1  

Here is the snip of the run, container ID,available containers using ps and execute the bash of the container's working directory.
In the working directory (etlcode), I added all the csv files.

    (venv) .\etl-pipeline>docker run --name dipriya_pillai -d -p 5000:5000 etlapp:v1
    882aac660dccd57cff0e3d6e01f77aee70503cdd5386c799927eb0abd2dce1f0

    (venv) .\etl-pipeline>docker ps
    CONTAINER ID   IMAGE       COMMAND             CREATED          STATUS          PORTS                    NAMES
    882aac660dcc   etlapp:v1   "python ./app.py"   19 seconds ago   Up 13 seconds   0.0.0.0:5000->5000/tcp   dipriya_pillai

    (venv) .\etl-pipeline>docker exec -it 882aac660dcc bash
    root@882aac660dcc:/etlcode# ls -l
    total 8
    -rwxr-xr-x 1 root root 2987 Jun 11 22:34 app.py
    -rwxr-xr-x 1 root root   30 Jun 11 20:18 requirements.txt
    root@882aac660dcc:/etlcode# mkdir data
    root@882aac660dcc:/etlcode# ls -l
    total 12
    -rwxr-xr-x 1 root root 2987 Jun 11 22:34 app.py
    drwxr-xr-x 2 root root 4096 Jun 11 23:21 data
    -rwxr-xr-x 1 root root   30 Jun 11 20:18 requirements.txt
    root@882aac660dcc:/etlcode# ls -l
    total 12
    -rwxr-xr-x 1 root root 2987 Jun 11 22:34 app.py
    drwxr-xr-x 2 root root 4096 Jun 11 23:01 data
    -rwxr-xr-x 1 root root   30 Jun 11 20:18 requirements.txt
    root@882aac660dcc:/etlcode# cd data
    root@882aac660dcc:/etlcode/data# ls -l
    total 12
    -rwxr-xr-x 1 root root 122 Jun 10 00:06 compounds.csv
    -rwxr-xr-x 1 root root 238 Jun 10 00:06 user_experiments.csv
    -rwxr-xr-x 1 root root 432 Jun 10 00:06 users.csv

**Step 4:**

All the csv's from ./data location in the project directory has been loaded and processed to get the dervied features using pandas' DataFrame **"processed_data"**. 

Further, the rows are iterated in the processed_data to get the results stored in **"data"**.

Then, created a **"create_conn()"** function that handles the connection to the postgres database along with error handling.

Using the **"create_conn()"** , created **cursor** object to execute postgres queries.

With the cursor object, I used the **execute()** function to create the table **"processed_data"** in public schema under **"userdata"** database and used the **executemany()** function to insert into **"processed_data"* table the final results.

Ran below command to debug and to **start the Flask app**


    python src/app.py

Here is the snip of the **run before triggering the ETL**  
 
     * Serving Flask app 'app'
     
     * Debug mode: on
    
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     
     * Running on all addresses (0.0.0.0)
     
     * Running on http://127.0.0.1:5000
     
     * Running on http://192.168.50.125:5000
    
    Press CTRL+C to quit
     
     * Restarting with stat
     
     * Debugger is active!
     
     * Debugger PIN: 509-399-788
    

**Step 5:**

Opened another terminal (CMD) and ran the following curl command to trigger the ETL process, the API end point is /trigger_etl and the connection is closed at last.

    curl -v http://localhost:5000/trigger_etl

Here is the snip of the output of the GET 

    (venv) .\etl-pipeline>curl -v http://localhost:5000/trigger_etl
    *   Trying 127.0.0.1:5000...
    * Connected to localhost (127.0.0.1) port 5000 (#0)
    > GET /trigger_etl HTTP/1.1
    > Host: localhost:5000
    > User-Agent: curl/8.0.1
    > Accept: */*
    >
    < HTTP/1.1 200 OK
    < Server: Werkzeug/2.3.6 Python/3.11.4
    < Date: Sun, 11 Jun 2023 23:26:31 GMT
    < Content-Type: application/json
    < Content-Length: 39
    < Connection: close
    <
    {
      "message": "ETL process started"
    }
    * Closing connection 0
    <
    {"message":"ETL process started"}
    * Closing connection 0

**Output at Flask app**

The following is the output **after triggering the ETL process through curl as shown above**.

**First snip** below shows the output message that **"11 Records inserted successfully."** which means the resulting iterated rows sucessfully inserted into the processed_data table in Postgres.

     python src/app.py
     
     * Serving Flask app 'app'
     
     * Debug mode: on
     
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
    
     * Running on all addresses (0.0.0.0)
     
     * Running on http://127.0.0.1:5000
     
     * Running on http://192.168.50.125:5000
     
    Press CTRL+C to quit
    
     * Restarting with stat
     
     * Debugger is active!
     
     * Debugger PIN: 509-399-788
     
    11 Records inserted successfully.
    
    127.0.0.1 - - [11/Jun/2023 18:28:36] "GET /trigger_etl HTTP/1.1" 200 -
    
**Second snip** below shows the output message that **"Records were already inserted and duplicate records are not valid."** which means the no duplicates are inserted into the processed_data table [as user_id is the PK] in Postgres.

The insert statement in postgres finds if there is any conflict in the insertion then it would do nothing.

     python src/app.py
     
     * Serving Flask app 'app'
     
     * Debug mode: on
     
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
    
     * Running on all addresses (0.0.0.0)
     
     * Running on http://127.0.0.1:5000
     
     * Running on http://192.168.50.125:5000
     
    Press CTRL+C to quit
    
     * Restarting with stat
     
     * Debugger is active!
     
     * Debugger PIN: 509-399-788
     
    Records were already inserted and duplicate records are not valid.
    
    127.0.0.1 - - [11/Jun/2023 18:28:36] "GET /trigger_etl HTTP/1.1" 200 -
    
    
    
    
