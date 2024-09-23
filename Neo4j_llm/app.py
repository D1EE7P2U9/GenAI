!pip install --upgrade --quiet  langchain langchain-community langchain-groq neo4j
%pip install -qU langchain-openai
!pip install --upgrade --quiet langchain_experimental
  

NEO4J_URI='your uri'
NEO4J_USERNAME='your username'
NEO4J_PASSWORD='your password'

from langchain_community.graphs import Neo4jGraph

graph=Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
)

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key="your_api_key"
    # base_url="...",
    # organization="...",
    # other params...
)

from langchain_core.documents import Document
text="""
Elon Reeve Musk (born June 28, 1971) is a businessman and investor known for his key roles in space
company SpaceX and automotive company Tesla, Inc. Other involvements include ownership of X Corp.,
formerly Twitter, and his role in the founding of The Boring Company, xAI, Neuralink and OpenAI.
He is one of the wealthiest people in the world; as of July 2024, Forbes estimates his net worth to be
US$221 billion.Musk was born in Pretoria to Maye and engineer Errol Musk, and briefly attended
the University of Pretoria before immigrating to Canada at age 18, acquiring citizenship through
his Canadian-born mother. Two years later, he matriculated at Queen's University at Kingston in Canada.
Musk later transferred to the University of Pennsylvania and received bachelor's degrees in economics
 and physics. He moved to California in 1995 to attend Stanford University, but dropped out after
  two days and, with his brother Kimbal, co-founded online city guide software company Zip2.
 """
documents=[Document(page_content=text)]
documents

from langchain_experimental.graph_transformers import LLMGraphTransformer
llm_transformer=LLMGraphTransformer(llm=llm)

graph_documents=llm_transformer.convert_to_graph_documents(documents)

graph_documents[0].nodes

### Load the dataset of movie

movie_query="""
LOAD CSV WITH HEADERS FROM
'https://raw.githubusercontent.com/tomasonjo/blog-datasets/main/movies/movies_small.csv' as row

MERGE(m:Movie{id:row.movieId})
SET m.released = date(row.released),
    m.title = row.title,
    m.imdbRating = toFloat(row.imdbRating)
FOREACH (director in split(row.director, '|') |
    MERGE (p:Person {name:trim(director)})
    MERGE (p)-[:DIRECTED]->(m))
FOREACH (actor in split(row.actors, '|') |
    MERGE (p:Person {name:trim(actor)})
    MERGE (p)-[:ACTED_IN]->(m))
FOREACH (genre in split(row.genres, '|') |
    MERGE (g:Genre {name:trim(genre)})
    MERGE (m)-[:IN_GENRE]->(g))
"""


graph.query(movie_query)

graph.refresh_schema()
print(graph.schema)


from langchain.chains import GraphCypherQAChain
chain=GraphCypherQAChain.from_llm(llm=llm,graph=graph,verbose=True,allow_dangerous_requests = True)
chain

response=chain.invoke({"query":"Who was the director of the moview GoldenEye"})

response

response=chain.invoke({"query":"tell me the genre of th movie GoldenEye"})

response
