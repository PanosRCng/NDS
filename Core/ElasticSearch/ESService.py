from elasticsearch import helpers

from Core.ElasticSearch.ES import ES
from Core.Logger import Logger




class ESService:


    @staticmethod
    def corpus_size(index_name):

        body = {
            "query": {
                "match_all": {}
            },
            "from": 0,
            "size": 1
        }

        res = ES.connection('es').search(index=index_name, body=body)

        return res['hits']['total']['value']


    @staticmethod
    def lexicon_terms(index_name):

        body = {
            "size": 0,
            "aggs": {
                "all_tokens": {
                    "terms": {
                        "field": "tokens",
                        "size": ESService.lexicon_size(index_name)
                    }
                }
            }
        }

        res = ES.connection('es').search(index=index_name, body=body)

        for term in res['aggregations']['all_tokens']['buckets']:
            yield {'word': term['key'], 'doc_count': term['doc_count']}


    @staticmethod
    def lexicon_size(index_name):

        body = {
            "aggs": {
                "total_tokens": {
                    "cardinality": {
                        "field": "tokens"
                    }
                }
            }
        }

        res = ES.connection('es').search(index=index_name, body=body)

        return res['aggregations']['total_tokens']['value']



    @staticmethod
    def create_index(name, config):

        try:

            if ES.connection('es').indices.exists(name):
                Logger.log(__name__, 'index ' + name + ' already exists', type='warning')
                return True

            ES.connection('es').indices.create(index=name, body=config)

        except Exception as ex:
            Logger.log(__name__, 'could not create index ' + name + '\t' + str(ex), type='error')
            return False

        return True


    @staticmethod
    def delete_index(name):

        try:

            if not ES.connection('es').indices.exists(name):
                Logger.log(__name__, 'index ' + name + ' does not exist', type='error')
                return False

            ES.connection('es').indices.delete(index=name)

        except Exception as ex:
            Logger.log(__name__, 'could not delete index ' + name + '\t' + str(ex), type='error')
            return False

