import os

from azure.identity import InteractiveBrowserCredential
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

import pandas as pd
import random
import sys
import json

import requests
load_dotenv()

class ACSClient:
    def __init__(self):
        credentials = InteractiveBrowserCredential()

        token = credentials.get_token("https://search.azure.com/.default")
        self.headers = {'Content-Type': 'application/json',
                        "Authorization": f"Bearer {token.token}"}
        self.api_version = f"?api-version={os.environ.get('AZURE_SEARCH_API_VERSION')}"
        self.index_name = os.environ.get('AZURE_SEARCH_INDEX_NAME')
        self.endpoint = f"https://{os.environ.get('AZURE_SEARCH_SERVICE_NAME')}.search.windows.net/"
        self.language_model = SentenceTransformer(os.environ.get('LANGUAGE_MODEL'), device="cpu")


    def create_search_index(self):

        with open("index-schema.json", 'r') as file:
            index_schema = json.load(file)

        index_schema["name"] = self.index_name

        url = f"{self.endpoint}indexes/{self.index_name}?api-version={self.api_version}"

        try:
            response = requests.put(url, headers=self.headers,
                                    json=index_schema)
            print(response.status_code)
        except Exception as e:
            print(f"Failed to create index: {e}")

    def prepare_data(self):
        df = pd.read_csv("data.csv")
        documents = []
        ctr = 0
        for index, row in df.iterrows():
            ctr += 1
            uuid = random.randint(df.shape[0] + 1, sys.maxsize)
            documents.append({"@search.action": "upload",
                         "objectUuid": str(uuid),
                         "commentId": str(ctr),
                         "comment": row["comments"],
                         "embeddings": self.language_model.encode(row["comments"]).tolist(),
                         })
        return documents

    def insert_documents(self, documents):

        url = self.endpoint + "indexes/" + self.index_name + "/docs/index" + self.api_version
        chunk = []
        ctr = 0
        for doc in documents:
            ctr += 1
            chunk.append(doc)
            if len(chunk) % 100 == 0:
                data = {"value": chunk}
                response = requests.post(url, headers=self.headers, json=data)
                print(
                    f"Attempted to upload {str(len(chunk))} documents, response code:{response.status_code}, processed {str(ctr)} documents")
                chunk = []
                # upload remaining documents
        data = {"value": chunk}
        response = requests.post(url, headers=self.headers, json=data)
        return response

    def search_documents(self, query):
        body = self.create_vector_search_payload(query)
        index_name = self.index_name
        url = self.endpoint + "/indexes/" + index_name + "/docs/search" + self.api_version
        azure_response = requests.post(url, headers=self.headers,
                                       json=body)
        resp = azure_response.json()
        comments = []
        for item in resp['value']:
            comments.append(item['comment'])
        context = "\n".join(comments)
        return context
    def create_vector_search_payload(self, query):
        """
        This method creates a request payload for an ACS Vector search
        """
        embeddings = self.language_model.encode(query).tolist()
        return {
            "vectorQueries": [
                {
                    "kind": "vector",
                    "vector": embeddings,
                    "exhaustive": True,
                    "fields": "embeddings",
                    "k": 100
                }
            ],
            "top": 100,
            "count": True,
            "select": "comment"
        }




if __name__ == "__main__":
    client = ACSClient()
    # client.create_search_index()
    # documents = client.prepare_data()
    # response = client.insert_documents(documents)
    resp = client.search_documents("what are they saying about work life balance?")
