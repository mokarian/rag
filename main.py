from acs import ACSClient
from llmclient import LLMClient

if __name__ == '__main__':
    acsclient = ACSClient()
    # create a search  index
    acsclient.create_search_index()
    # read data and prepare data to ingest
    documents = acsclient.prepare_data()
    #Insret data into ACS
    response = acsclient.insert_documents(documents)

    question = "what are they saying about promotions?"
    print(question)
   # Call Azure Search Service to get the context
    context = acsclient.search_documents(query=question)
    llm_client = LLMClient()
    # Send the full prompt to LLM and get the answer
    answer = llm_client.ask(question, context)
    print(answer)


