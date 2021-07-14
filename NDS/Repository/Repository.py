import datetime
from datetime import timezone

from Core.Config import Config
from Core.Logger import Logger
from NDS.Stopwords import Stopwords
from NDS.Repository.Stoplist import Stoplist
from NDS.Repository.FSStore import FSStore




class Repository:


    __instance = None


    def __init__(self):

        if Repository.__instance is not None:
            return

        Repository.__instance = self
        self.__setup()


    @staticmethod
    def __get_instance():

        if Repository.__instance is None:
            Repository()

        return Repository.__instance


    @staticmethod
    def list():
        return Repository.__get_instance().__list()


    @staticmethod
    def get(alias):
        return Repository.__get_instance().__get(alias)


    @staticmethod
    def version(alias):
        return Repository.__get_instance().__current_version(alias)


    @staticmethod
    def update(alias):
        return Repository.__get_instance().__update(alias)



    def __setup(self):

        self.__stoplists = {}

        for alias in Config.get('nds')['stopwords']:

            stoplist = FSStore.load(alias)

            if stoplist is None:
                stoplist = self.__create(alias)
            else:
                Logger.log(__name__, 'loaded ' + alias + ' version ' + stoplist.version)

            self.__stoplists[alias] = stoplist


    def __list(self):
        return list(self.__stoplists.keys())


    def __get(self, alias):
        return self.__stoplists[alias].terms


    def __current_version(self, alias):
        return self.__stoplists[alias].version


    def __update(self, alias):

        FSStore.remove(alias)

        self.__stoplists[alias] = self.__create(alias)



    def __create(self, alias):

        stoplist = Stoplist(alias, Stopwords.calculate(alias), str(self.__now_utc_timestamp()))

        FSStore.store(stoplist)

        Logger.log(__name__, 'new version created ' + stoplist.version + ' for ' + alias)

        return stoplist



    def __now_utc_timestamp(self):
        return int(datetime.datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())


