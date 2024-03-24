# NeuroKG
Building knowledge graphs from neuroscience papers to gain more insides about interconnections between papers and new knowledge.

## Install the project
### Update .env file
You should include OPENAI_API_KEY and credential for Neo4j database (User is mostly Neo4j, Password and URL as bolt://localhost:xxxx).
### Install requirements
I will add them later.
## Run the project
This code contains 4 pipelines  
Firstly, you should run in terminal pipeline to parse pdf files to txt transformed by OpenAI model. You shoukd add papers in pdf to the folder data/pdf_papers
```python
python3 -m pipeline.pipeline_pdf_to_parsed_txt
```
Then, you run pipeline to transform txt to knowledge graph and store in Neo4j
```python
python3 -m pipeline.pipeline_parsed_txt_to_graph
```
Third pipeline will be in Jupyter Notebook with descriptional statistics of the graph (diameter, radius, number of V and E, etc.)

Forth pipeline will be also in Jupyter Notebook with specific queries to the graph.
