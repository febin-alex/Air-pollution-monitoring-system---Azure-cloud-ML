from keep_alive import keep_alive
import azure
import pandas as pd
import azure.storage.blob
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from datetime import datetime
import csv
import pickle
import statistics
from statistics import mode
import time
filename='model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
keep_alive()
import datetime
import pytz



while True:
  


    conn_str = 'DefaultEndpointsProtocol=https;AccountName=mqiotstorage;AccountKey=hhttmBT+2eSvJWt2emV7aiy2ygJBknYfDsPgVrtGBHm8FpVC785Z20Z8ZDmqmibiQFmIolSuWGyE+AStMjqvBw==;EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    
    blob_list = blob_service_client.get_container_client('mqcontainer').list_blobs()
    for blob in blob_list:
        blobname=blob.name
        blob = BlobClient(account_url="https://mqiotstorage.blob.core.windows.net",
                      container_name="mqcontainer",
                      blob_name=blobname,
                      credential="hhttmBT+2eSvJWt2emV7aiy2ygJBknYfDsPgVrtGBHm8FpVC785Z20Z8ZDmqmibiQFmIolSuWGyE+AStMjqvBw==")
        with open("input.csv", "wb") as f:
          data = blob.download_blob()
          data.readinto(f)
    
    with open('input.csv') as file_obj:
    
    
        reader_obj = csv.reader(file_obj)
        w, h = 2, 100
        a = [[0 for x in range(w)] for y in range(h)]
        j=0
        k=0
        flag=0
        flag1=0
    
        for row in reader_obj:
          flag+=1
          if(flag%2!=0):
            k=0
            for i in row:
              if(k==0):
                a[j][k]=i
                a[j][k]=str(a[j][k])
                a[j][k]=a[j][k][8:]
                k=1
              break
             
          else:
            k=0
            for i in row:
              if(k==0):
                k=1
                continue
              else:
                a[j][k]=i
                a[j][k]=str(a[j][k])
                a[j][k]=a[j][k][6:-1] 
            
                
            j+=1
          
      
    
    
    filename = "mqfinal.csv"
    m=0
    fields = ['mq2', 'mq135']
    
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        while(m<j):
           rows = [ [int(a[m][0]),int(a[m][1])] ]
           csvwriter.writerows(rows)
           m+=1
    
    
    
    
    
    
    
    
    df=pd.read_csv('mqfinal.csv')
    predictions=loaded_model.predict(df)
    
    
    
    value=mode(predictions)
    print(value)
    
    
    current_time = datetime.datetime.now(pytz.timezone('Asia/Calcutta'))
    dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
    

    filename = "output.csv"


    with open(filename, 'w') as csvfile: 
          csvwriter = csv.writer(csvfile) 
          rows = [ [int(a[j-1][0]),int(a[j-1][1]),str(value),str(dt_string)] ]
          csvwriter.writerows(rows)
      
      
    conn_str = 'DefaultEndpointsProtocol=https;AccountName=mqiotstorage;AccountKey=hhttmBT+2eSvJWt2emV7aiy2ygJBknYfDsPgVrtGBHm8FpVC785Z20Z8ZDmqmibiQFmIolSuWGyE+AStMjqvBw==;EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
          
    blob_client = blob_service_client.get_blob_client(container='mqwebcontainer', blob='output.csv')
    with open('output.csv', "rb") as data:
          blob_client.upload_blob(data,overwrite=True)
          
          

    filenam = "total.csv"
   


    with open(filenam, 'a') as csvfile: 
          csvwriter = csv.writer(csvfile) 
          rows = [ [int(a[j-1][0]),int(a[j-1][1]),str(value), str(dt_string)] ]
          csvwriter.writerows(rows)



    
    
    time.sleep(3600)
