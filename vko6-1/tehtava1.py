import requests
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.resource import ResourceManagementClient
import os


#Haetaan JSON data

r = requests.get("https://2ri98gd9i4.execute-api.us-east-1.amazonaws.com/dev/academy-checkpoint2-json")

data = r.json() 

#Luetaan datasta parameter kenttien arvot ja kirjoitetaan ne checkpoint.txt tiedostoon omille riveilleen

with open("checkpoint.txt", "w") as tiedosto:
    for i in data['items']:
        tiedosto.write(i['parameter'])
        tiedosto.write("\n")

#Luodaan uusi RG Azureen

credential = DefaultAzureCredential()

subscription_id = os.environ["SUBSCRIPTION_ID"]

resource_client = ResourceManagementClient(credential, subscription_id)

storage_client = StorageManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=os.environ["SUBSCRIPTION_ID"]
    )


resource_client.resource_groups.create_or_update(
    "annacheckpointrg",
    {"location": "westeurope"}
    )

#Luodaan storage account

storage_client.storage_accounts.begin_create(
    "annacheckpointrg",
    "annastorageacc01",
    {
        "sku": {
        "name": "Standard_GRS"
        },
        "kind": "StorageV2",
        "location": "westeurope",
        "encryption": {
        "services": {
            "file": {
            "key_type": "Account",
            "enabled": True
            },
            "blob": {
            "key_type": "Account",
            "enabled": True
            }
        },
        "key_source": "Microsoft.Storage"
        },
        "tags": {
        "key1": "value1",
        "key2": "value2"
        }
    }
).result()
    

#Luodaan blob container

blob_container = storage_client.blob_containers.create(
    "annacheckpointrg",
    "annastorageacc01",
    "annacontainer01",
    {}
)
print("Create blob container:\n{}".format(blob_container))

#Tallennetaan checkpoint.txt tiedosto blob containeriin

def uploadblob(tiedosto):
    from azure.storage.blob import BlobClient

    blob = BlobClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;AccountName=annastorageacc01;AccountKey=KKeVZ6D4ykJOo0PbxJ3mzPdEKmWyoVbMWH+9JPGoArz6dgExbWN3CXWK7a25xAyf1lo/iOHBIui7xIU6qy2y8Q==;EndpointSuffix=core.windows.net", container_name="annacontainer01", blob_name="checkpoint.txt")

    with open(tiedosto, "rb") as data:
        blob.upload_blob(data)
        print("Update blob container:\n{}".format("annastorageacc01"))
    
uploadblob("./checkpoint.txt")



