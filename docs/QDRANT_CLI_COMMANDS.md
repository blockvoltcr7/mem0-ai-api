# Qdrant CLI Commands & HTTP API Reference

This document provides comprehensive commands for interacting with your Qdrant database deployed on Railway without using Python.

## Database Information
- **URL**: `https://qdrant-production-3e2f.up.railway.app`
- **Protocol**: HTTPS
- **Port**: 443 (default HTTPS)

## Quick Health Check

### Test Connection
```bash
curl -s https://qdrant-production-3e2f.up.railway.app/
```

### Get Database Status
```bash
curl -s https://qdrant-production-3e2f.up.railway.app/ | python3 -m json.tool
```

## Collection Management

### 1. List All Collections
```bash
# Basic list
curl -X GET https://qdrant-production-3e2f.up.railway.app/collections

# Pretty formatted (requires python3)
curl -s https://qdrant-production-3e2f.up.railway.app/collections | python3 -m json.tool

# Using jq (if installed)
curl -s https://qdrant-production-3e2f.up.railway.app/collections | jq '.'
```

### 2. Get Collection Information
```bash
# Replace {collection_name} with actual collection name
curl -X GET https://qdrant-production-3e2f.up.railway.app/collections/{collection_name}

# Example for a collection named "mem0_collection"
curl -X GET https://qdrant-production-3e2f.up.railway.app/collections/mem0_collection
```

### 3. Check if Collection Exists
```bash
curl -X GET https://qdrant-production-3e2f.up.railway.app/collections/{collection_name}/exists
```

### 4. Create a Collection
```bash
# Basic collection with vector size 1536 (OpenAI embeddings)
curl -X PUT https://qdrant-production-3e2f.up.railway.app/collections/{collection_name} \
  -H 'Content-Type: application/json' \
  --data-raw '{
    "vectors": {
      "size": 1536,
      "distance": "Cosine"
    }
  }'

# Collection with custom configuration
curl -X PUT https://qdrant-production-3e2f.up.railway.app/collections/{collection_name} \
  -H 'Content-Type: application/json' \
  --data-raw '{
    "vectors": {
      "size": 1536,
      "distance": "Cosine"
    },
    "optimizers_config": {
      "indexing_threshold": 20000
    },
    "replication_factor": 1
  }'
```

### 5. Delete a Collection
```bash
curl -X DELETE https://qdrant-production-3e2f.up.railway.app/collections/{collection_name}
```

### 6. Update Collection Parameters
```bash
curl -X PATCH https://qdrant-production-3e2f.up.railway.app/collections/{collection_name} \
  -H 'Content-Type: application/json' \
  --data-raw '{
    "optimizers_config": {
      "indexing_threshold": 10000
    }
  }'
```

## Points Management

### 1. Count Points in Collection
```bash
curl -X POST https://qdrant-production-3e2f.up.railway.app/collections/{collection_name}/points/count \
  -H 'Content-Type: application/json' \
  --data-raw '{}'
```

### 2. Search Points
```bash
curl -X POST https://qdrant-production-3e2f.up.railway.app/collections/{collection_name}/points/search \
  -H 'Content-Type: application/json' \
  --data-raw '{
    "vector": [0.1, 0.2, 0.3, ...],
    "limit": 10
  }'
```

### 3. Get Point by ID
```bash
curl -X GET https://qdrant-production-3e2f.up.railway.app/collections/{collection_name}/points/{point_id}
```

### 4. Scroll Through Points
```bash
curl -X POST https://qdrant-production-3e2f.up.railway.app/collections/{collection_name}/points/scroll \
  -H 'Content-Type: application/json' \
  --data-raw '{
    "limit": 100,
    "with_payload": true,
    "with_vector": false
  }'
```

## Aliases Management

### 1. List All Aliases
```bash
curl -X GET https://qdrant-production-3e2f.up.railway.app/aliases
```

### 2. List Collection Aliases
```bash
curl -X GET https://qdrant-production-3e2f.up.railway.app/collections/{collection_name}/aliases
```

### 3. Create Alias
```bash
curl -X POST https://qdrant-production-3e2f.up.railway.app/collections/aliases \
  -H 'Content-Type: application/json' \
  --data-raw '{
    "actions": [
      {
        "create_alias": {
          "collection_name": "actual_collection_name",
          "alias_name": "my_alias"
        }
      }
    ]
  }'
```

### 4. Delete Alias
```bash
curl -X POST https://qdrant-production-3e2f.up.railway.app/collections/aliases \
  -H 'Content-Type: application/json' \
  --data-raw '{
    "actions": [
      {
        "delete_alias": {
          "alias_name": "my_alias"
        }
      }
    ]
  }'
```

## Cluster Information

### 1. Get Cluster Info
```bash
curl -X GET https://qdrant-production-3e2f.up.railway.app/cluster
```

### 2. Get Collection Cluster Info
```bash
curl -X GET https://qdrant-production-3e2f.up.railway.app/collections/{collection_name}/cluster
```

## Snapshots

### 1. List Snapshots
```bash
curl -X GET https://qdrant-production-3e2f.up.railway.app/collections/{collection_name}/snapshots
```

### 2. Create Snapshot
```bash
curl -X POST https://qdrant-production-3e2f.up.railway.app/collections/{collection_name}/snapshots
```

### 3. Delete Snapshot
```bash
curl -X DELETE https://qdrant-production-3e2f.up.railway.app/collections/{collection_name}/snapshots/{snapshot_name}
```

## Useful Scripts

### Quick Collection Check Script
Save this as `check_collections.sh`:
```bash
#!/bin/bash
QDRANT_URL="https://qdrant-production-3e2f.up.railway.app"

echo "📊 Qdrant Collections Summary"
echo "=============================="

# Get collections
RESPONSE=$(curl -s "$QDRANT_URL/collections")
echo "Raw response: $RESPONSE"

# Extract collection names and get details
echo "$RESPONSE" | grep -o '"name":"[^"]*"' | cut -d'"' -f4 | while read -r collection; do
    if [ -n "$collection" ]; then
        echo "Collection: $collection"
        curl -s "$QDRANT_URL/collections/$collection" | grep -o '"points_count":[0-9]*\|"status":"[^"]*"' | tr '\n' ' '
        echo ""
    fi
done
```

### Memory Usage Check
```bash
#!/bin/bash
QDRANT_URL="https://qdrant-production-3e2f.up.railway.app"

curl -s "$QDRANT_URL/collections" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if 'result' in data and 'collections' in data['result']:
    for collection in data['result']['collections']:
        name = collection['name']
        info = json.loads(sys.stdin.read()) if False else {}
        print(f'Collection: {name}')
"
```

## Common Use Cases

### Find Mem0 Collections
```bash
curl -s https://qdrant-production-3e2f.up.railway.app/collections | grep -i mem0
```

### Check Collection Health
```bash
COLLECTION_NAME="your_collection_name"
curl -s https://qdrant-production-3e2f.up.railway.app/collections/$COLLECTION_NAME | \
  python3 -c "import json, sys; data=json.load(sys.stdin); print(f\"Status: {data['result']['status']}, Points: {data['result']['points_count']}\")"
```

### Monitor All Collections
```bash
for collection in $(curl -s https://qdrant-production-3e2f.up.railway.app/collections | grep -o '"name":"[^"]*"' | cut -d'"' -f4); do
  echo "Checking $collection..."
  curl -s https://qdrant-production-3e2f.up.railway.app/collections/$collection | grep -o '"status":"[^"]*"\|"points_count":[0-9]*'
done
```

## Error Handling

### Check HTTP Status
```bash
curl -w "HTTP Status: %{http_code}\n" -s https://qdrant-production-3e2f.up.railway.app/collections
```

### Verbose Output for Debugging
```bash
curl -v https://qdrant-production-3e2f.up.railway.app/collections
```

## Notes

1. **No Authentication Required**: Your Railway deployment appears to be publicly accessible
2. **HTTPS Only**: Always use `https://` prefix
3. **JSON Responses**: All responses are in JSON format
4. **Rate Limiting**: Be mindful of making too many requests in quick succession
5. **Collection Names**: Replace `{collection_name}` with actual collection names from your database

## Quick Reference Commands

```bash
# Most common commands for daily use:

# 1. List collections
curl -s https://qdrant-production-3e2f.up.railway.app/collections | python3 -m json.tool

# 2. Check specific collection
curl -s https://qdrant-production-3e2f.up.railway.app/collections/COLLECTION_NAME | python3 -m json.tool

# 3. Count points in collection
curl -X POST https://qdrant-production-3e2f.up.railway.app/collections/COLLECTION_NAME/points/count \
  -H 'Content-Type: application/json' --data-raw '{}'

# 4. Check database health
curl -s https://qdrant-production-3e2f.up.railway.app/ | python3 -m json.tool
```

---

**Last Updated**: January 2025  
**Qdrant Version**: Compatible with v1.7+  
**Railway URL**: `https://qdrant-production-3e2f.up.railway.app` 