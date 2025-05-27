As a developer i want to use mem0 as a vector database store to allow users to chat with ai agents and retain memory of previous conversations.

code example:

import os
from dotenv import load_dotenv
from openai import OpenAI
from mem0 import Memory

# 1. bootstrap
load_dotenv()
client = OpenAI()  # uses OPENAI_API_KEY

# 2. configure Mem0 → Qdrant
memory = Memory.from_config({
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "test_smoke",    # optional, but good practice
            "host": os.getenv("QDRANT_HOST"),
            "port": int(os.getenv("QDRANT_PORT")),
        }
    }
})
print("✅ Memory layer initialized with Qdrant")

# 3. add a sample memory
memory.add("My first memory entry", metadata={"test":"yes"})
print("✅ Added a memory")

# 4. search for it
results = memory.search("first memory", k=1)
print("🔍 Search results:", [r["text"] for r in results])


task: create a pytest to test this is working as expdcted

currently the quadrant database is deployed locally on a docker container:


CONTAINER ID   IMAGE              COMMAND                  CREATED        STATUS          PORTS                    NAMES
810aa7b1d4d2   n8nio/n8n:latest   "tini -- /docker-ent…"   5 months ago   Up 10 seconds   0.0.0.0:5678->5678/tcp   yaml_files-n8n-1
☁  ~  docker run -d --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  qdrant/qdrant

Unable to find image 'qdrant/qdrant:latest' locally
latest: Pulling from qdrant/qdrant
b16f1b166780: Pull complete
a6e17ca61522: Pull complete
4f4fb700ef54: Pull complete
003dba7d7b22: Pull complete
13573604b890: Pull complete
44113adf5a0e: Pull complete
a60c2e005c05: Pull complete
dc84f73ed3cf: Pull complete
Digest: sha256:419d72603f5346ee22ffc4606bdb7beb52fcb63077766fab678e6622ba247366
Status: Downloaded newer image for qdrant/qdrant:latest
ea4bd0bb22f593477a0d830751eb1304dd90daf07346498cdcc67693fadab2be
☁  ~  curl http://localhost:6333/collections

{"result":{"collections":[]},"status":"ok","time":0.000027167}



Instructions:

1. create a new pytest to test mem0
2. run the test and open the allure report


[X] Task Completed
