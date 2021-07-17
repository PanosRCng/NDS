from json import loads

from kafka import KafkaConsumer

from Core.Config import Config
from Core.Logger import Logger
from Core.ElasticSearch.ES import ES
from Core.ElasticSearch.ESService import ESService
from NDS.Tokenizers.Tokenizer import Tokenizer




class Feeder:


    @staticmethod
    def feed(alias):

        if alias not in Config.get('nds')['stopwords']:
            Logger.log(__name__, alias + ' feed does not exist', type='error')
            return

        stopwords_config = Config.get('nds')['stopwords'][alias]

        Logger.log(__name__, 'starting feed ' + alias)

        if ES.connection('es') is None:
            Logger.log(__name__, 'could not connect to elasticsearch', type='error')
            return

        index_name = stopwords_config['elasticsearch_index']
        kafka_topic = stopwords_config['kafka_topic']

        ESService.create_index(index_name, Config.get('elasticsearch')['indices_settings'][index_name])

        kafka_server = Config.get('kafka')['server'] + ':' + str(Config.get('kafka')['port'])

        kafkaConsumer = KafkaConsumer(kafka_topic,
                                      auto_offset_reset='earliest',
                                      enable_auto_commit=True,
                                      auto_commit_interval_ms=1000,
                                      group_id='my-group2',
                                      value_deserializer=lambda x: loads(x.decode('utf-8')),
                                      bootstrap_servers=kafka_server)

        tokenizer = Tokenizer.create(stopwords_config['tokenizer'])

        for msg in kafkaConsumer:

            article = msg.value

            tokens = tokenizer.tokenize(article['title']) + tokenizer.tokenize(article['content'])

            if len(tokens) < stopwords_config['text_min_tokens_number']:
                continue

            Logger.log(__name__, alias + ' feed' + '\t' + str(len(tokens)) + ' tokens\t' + article['title'])

            Feeder.save_tokens(tokens, index_name)


    @staticmethod
    def save_tokens(tokens, index_name):

        body = {
            'tokens': ' '.join(tokens)
        }

        ES.connection('es').index(index_name, body=body)


