ES_HOST = 'thedsk8-es-3821586929.us-east-1.bonsaisearch.net'
ES_PORT = 443
ES_ACCESS_KEY = 'DMfxP7CwEa'
ES_ACCESS_SECRET = 'GiKvLERrusVWc3H7N8tBkgT'
ES_INDEX = 'queries'
ES_INDEX_MAPPING = {
    "properties": {
      "user_id": {
        "type": "keyword"
      },
      "time": {
        "type": "date"
      },
      "query": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      }
    }
  }
ES_INDEX_SETTINGS = {
    "number_of_replicas": 1,
    "number_of_shards": 1
  }