import os

from azure.identity import InteractiveBrowserCredential
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

class LLMClient:
    def __init__(self):
        credentials = InteractiveBrowserCredential()

        token = credentials.get_token("https://cognitiveservices.azure.com/.default")
        self.client = AzureOpenAI(
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
            azure_ad_token=token.token,
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        )

    def ask(self, question, context):
        prompt = self.read_file("prompt.txt")
        prompt = prompt.replace("~~~comments_text~~~", context)
        response = self.client.chat.completions.create(
            model="gpt-4o",  # model = "deployment_name".
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content

    def read_file(self, filename):
        with open(filename, 'r') as content_file:
            content = content_file.read()
        return content
