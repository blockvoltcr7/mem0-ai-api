#!/bin/bash

# Qdrant Direct HTTP API Checker
# Usage: ./check_qdrant_direct.sh

QDRANT_URL="https://qdrant-production-3e2f.up.railway.app"

echo "🔍 Checking Qdrant Database Status..."
echo "=================================="

# Check if Qdrant is accessible
echo "1. Testing Qdrant Connection:"
curl -s -w "HTTP Status: %{http_code}\n" "$QDRANT_URL/" || echo "❌ Connection failed"

echo -e "\n2. Listing All Collections:"
curl -s "$QDRANT_URL/collections" | python3 -m json.tool 2>/dev/null || curl -s "$QDRANT_URL/collections"

echo -e "\n3. Checking for Mem0 Collections:"
COLLECTIONS=$(curl -s "$QDRANT_URL/collections" | grep -o '"name":"[^"]*"' | cut -d'"' -f4)

if [ -n "$COLLECTIONS" ]; then
    echo "Found collections:"
    echo "$COLLECTIONS" | while read -r collection; do
        if [ -n "$collection" ]; then
            echo "  - $collection"
            echo "    Info: $(curl -s "$QDRANT_URL/collections/$collection" | grep -o '"points_count":[0-9]*' | cut -d':' -f2) points"
        fi
    done
else
    echo "No collections found or unable to parse response"
fi

echo -e "\n4. Raw Collections Response:"
curl -s "$QDRANT_URL/collections"

echo -e "\n\n✅ Check complete!" 