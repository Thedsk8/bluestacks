import datetime
from elasticsearch import Elasticsearch
from settings import ES_HOST, ES_PORT, ES_ACCESS_KEY, ES_ACCESS_SECRET


def get_es_client():
    """
    :return: return elastic search client
    """
    connection_config = [{
      'host': ES_HOST,
      'port': ES_PORT,
      'use_ssl': True,
      # These should not be kept here, should be kept securely.
      'http_auth': (ES_ACCESS_KEY, ES_ACCESS_SECRET)},
    ]
    es_client = Elasticsearch(connection_config)
    return es_client


def create_elastic_index(client, index, settings, mappings):
    """
    Create index on elastic search
    :param index: name of index
    :param settings: settings of index
    :param mappings: mapping of index
    :return:
    """
    response = {'success': True, 'error': ''}
    try:
        body = {"settings": settings, "mappings": mappings}
        client.indices.create(index=index, body=body)
    except Exception as e:
        response.update({'success': False, 'error': e})
    return response


def get_elasticsearch_doc(query, client_id):
    """
    :param query: query field on which google search was made
    :param client_id: id of the client who made that search
    :return: document to be indexed on elasticsearch
    """
    document = {
        "user_id": client_id,
        "time": datetime.datetime.now(),
        "query": query
    }

    return document


def write_to_elasticsearch(index, document):
    """
    Writes document to elasticsearch
    :param index: index name on which data needs to be indexed
    :param document: documnet which has to be indexed
    :return: response
    """
    es = get_es_client()
    resp = es.index(index=index,body=document)
    return resp


def get_documents_from_elasticsearch(index, query, client_id):
    """
    get recent searches of the given user that matches query ordered by time
    in ascending order
    Using "match" here so if anything is matched it will be there in the
    result, as results are ordered by time, document which matches the most
    might not be on top.
    :param index: name
    :param query: query name
    :param client_id: user id
    :return: documents from elastic search
    """
    res = {}
    body = {
              "query": {
                "bool": {
                  "must": [
                    {
                      "term": {
                        "user_id": {
                          "value": client_id
                        }
                      }
                    },
                    {
                      "match": {
                          "query": query
                      }
                    }
                  ]
                }
              },
              "sort": [
                {
                  "time": {
                    "order": "asc"
                  }
                }
              ]
            }
    try:
        es = get_es_client()
        # timeout increased due to small db size
        res = es.search(index=index, body=body, request_timeout=60)
    except Exception as e:
        # log exception and create retry mechanism
        res.update({'exception':
                        'Exception occured {} \n Please try again!!!'.format(e)
                    })

    return res
