import argparse
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.resource import ResourceManagementClient

import os

#Komentorivi käyttöön

parser = argparse.ArgumentParser()

parser.add_argument("luku", help="Anna tulostettavien rivien lkm", type=int)

args = parser.parse_args()

lkm = int(args.luku)

#Ladataan checkpoint.txt blob containerista

credential = DefaultAzureCredential()

subscription_id = os.environ["SUBSCRIPTION_ID"]

resource_client = ResourceManagementClient(credential, subscription_id)

storage_client = StorageManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=os.environ["SUBSCRIPTION_ID"]
    )

def downblob(file):
    from azure.storage.blob import BlobClient

    blob = BlobClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;AccountName=annastorageacc01;AccountKey=KKeVZ6D4ykJOo0PbxJ3mzPdEKmWyoVbMWH+9JPGoArz6dgExbWN3CXWK7a25xAyf1lo/iOHBIui7xIU6qy2y8Q==;EndpointSuffix=core.windows.net", container_name="annacontainer01", blob_name=file)

    with open("./checkpoint.txt", "wb") as file:
        blob_data = blob.download_blob()
        blob_data.readinto(file)
    
downblob("checkpoint.txt")

#Tulostetaan checkpoint.txt tiedostosta

with open("checkpoint.txt") as tiedosto:
    data = tiedosto.read()
    for i in data['items']:
        while i <= lkm:
            lista = tiedosto.read(i['parameter'])
    
    lista.sort()
    print(lista)

#Ja aika loppui...