from Core.Config import Config
from Core.ElasticSearch.ESService import ESService
from Core.TermInformativeness import TermInformativeness



class Stopwords:


    @staticmethod
    def calculate(alias, no_score=False):

        elasticsearch_index = Config.get('nds')['stopwords'][alias]['elasticsearch_index']

        if no_score is True:
            return [term['word'] for term in ESService.lexicon_terms(elasticsearch_index, max_terms=Config.get('nds')['stopwords'][alias]['max_terms'])]

        corpus_size = ESService.corpus_size(elasticsearch_index)

        terms = {}
        for term in ESService.lexicon_terms(elasticsearch_index, max_terms=Config.get('nds')['stopwords'][alias]['max_terms']):
            terms[term['word']] = TermInformativeness.normalised_idf(corpus_size, term['doc_count'])

        return terms


