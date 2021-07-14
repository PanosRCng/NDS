from Core.Config import Config
from Core.ElasticSearch.ESService import ESService
from Core.TermInformativeness import TermInformativeness



class Stopwords:


    @staticmethod
    def calculate(alias):

        elasticsearch_index = Config.get('nds')['stopwords'][alias]['elasticsearch_index']

        corpus_size = ESService.corpus_size(elasticsearch_index)

        terms = {}
        for term in ESService.lexicon_terms(elasticsearch_index):
            terms[term['word']] = TermInformativeness.normalised_idf(corpus_size, term['doc_count'])

        sorted_terms = dict(sorted(terms.items(), key=lambda item: item[1]))

        return list(sorted_terms.keys())[:Config.get('nds')['stopwords'][alias]['max_terms']]

