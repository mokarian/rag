# RAG Architecture Demo with Azure OpenAI and Azure Cognitive Search

## Overview

This demo showcases a Retrieval-Augmented Generation (RAG) architecture implemented using Azure OpenAI and Azure Cognitive Search (ACS). It highlights how a search index and a language model can be combined to provide contextual and accurate answers to user queries. The two key Python modules in this project, `acs.py` and `llmclient.py`, interact to achieve this functionality.

### Key Components
1. **Azure Cognitive Search (ACS)**:
    - Acts as the retrieval component of the RAG pipeline.
    - Stores a searchable index of documents.
    - Uses a transformer model to generate vector embeddings for semantic search.

2. **Azure OpenAI (LLM)**:
    - Provides the generation component of the RAG pipeline.
    - Uses GPT-4 for natural language understanding and text generation.

3. **Transformer Model**:
    - The `all-MiniLM-L6-v2` model is used to create vector embeddings from text.

## Files and Their Responsibilities

### 1. `acs.py`
This module manages interactions with Azure Cognitive Search.

- **Core Responsibilities:**
    - **Index Creation**:
      Creates a new search index using a schema defined in `index-schema.json`.
    - **Data Preparation**:
      Reads data from a CSV file, generates embeddings for each document, and formats the data for indexing.
    - **Data Ingestion**:
      Inserts prepared documents into the Azure Cognitive Search index.
    - **Semantic Search**:
      Performs vector-based semantic searches on the indexed data and retrieves relevant documents as context for generation.

### 2. `llmclient.py`
This module manages interactions with Azure OpenAI's GPT-based models.

- **Core Responsibilities:**
    - **Prompt Creation**:
      Reads a predefined prompt template from `prompt.txt` and replaces placeholders with contextual data from ACS.
    - **Answer Generation**:
      Uses the GPT model to generate answers to user questions based on the context provided by ACS.

### 3. Main Script
The main script demonstrates the interaction between ACS and Azure OpenAI:
- A question is passed to the ACS client, which retrieves relevant contextual information.
- The context is then fed into the LLM client, which generates an answer.

## RAG Architecture

### What is RAG?
Retrieval-Augmented Generation (RAG) is an architecture where retrieval and generation components work together to provide accurate and context-aware responses. It enhances the performance of language models by grounding their outputs in external knowledge sources.

### Workflow in This Demo:
1. **Document Indexing**:
    - Data is preprocessed and indexed in Azure Cognitive Search.
    - The `all-MiniLM-L6-v2` transformer model generates vector embeddings for semantic search.

2. **Query Processing**:
    - A user query is sent to the ACS client.
    - ACS performs a vector search to find the most relevant documents.

3. **Contextual Response Generation**:
    - The retrieved documents are passed as context to the GPT-based Azure OpenAI model.
    - The model generates a response grounded in the provided context.

### Advantages of RAG:
- **Accuracy**: Combines external knowledge with LLM capabilities.
- **Efficiency**: Leverages vector search for quick and relevant document retrieval.
- **Scalability**: Supports large datasets and complex queries.

## Setup and Usage

### Prerequisites
1. **Azure Resources:**
   - Azure OpenAI service with GPT-4 deployed.
   - Azure Cognitive Search service.

2. **Python Libraries:**
   - `azure-identity`
   - `sentence-transformers`
   - `pandas`
   - `requests`
   - `python-dotenv`

3. **Environment Variables:**
   - `AZURE_SEARCH_API_VERSION`
   - `AZURE_SEARCH_INDEX_NAME`
   - `AZURE_SEARCH_SERVICE_NAME`
   - `LANGUAGE_MODEL` (Set to `all-MiniLM-L6-v2`)
   - `AZURE_OPENAI_ENDPOINT`
   - `AZURE_OPENAI_API_VERSION`

### Steps to Run the Demo
1. Clone the repository and navigate to the project directory.
2. Set up the required environment variables in a `.env` file.
3. Prepare your data:
    - Place the dataset in `data.csv`.
    - Define the index schema in `index-schema.json`.
4. Run the main script:
    ```bash
    python main.py
    ```

### Example Interaction
- **Input Question**: "What are they saying about promotions?"
- **Output**:
    - The ACS client retrieves documents relevant to "promotions."
    - The LLM client uses these documents to generate a detailed and contextual response.

## Conclusion
This project demonstrates the power of the RAG architecture by combining Azure Cognitive Search and Azure OpenAI. It is a scalable and efficient approach to building applications that require accurate, context-aware responses grounded in external data.

