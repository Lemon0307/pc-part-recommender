from neo4j import GraphDatabase

URI = "neo4j://127.0.0.1:7687"

# change in final version
AUTH = ("neo4j", "51111088")

driver = GraphDatabase.driver(URI, auth=AUTH)

def get_driver(): 
    return driver