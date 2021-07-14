import os
import json
import datetime
from datetime import timezone

import requests




class Stopwords:


    version_TTL_hours = 10
    service_url = 'http://192.168.1.12:8000/nds'
    local_copy_dir = 'stopwords'


    __instance = None


    def __init__(self):

        if Stopwords.__instance is not None:
            return

        Stopwords.__instance = self
        self.__setup()


    @staticmethod
    def __get_instance():

        if Stopwords.__instance is None:
            Stopwords()

        return Stopwords.__instance


    @staticmethod
    def get(alias):
        return Stopwords.__get_instance().__get(alias)



    def __setup(self):

        self.__stoplists = {}

        for alias in requests.get(Stopwords.service_url + '/list').json():

            stoplist = self.__load(alias)

            if stoplist is None:
                stoplist = self.__fetch(alias)

            self.__stoplists[alias] = stoplist


    def __get(self, alias):

        if alias not in self.__stoplists.keys():
            self.__stoplists[alias] = self.__fetch(alias)
        else:
            if self.__is_outdated(self.__stoplists[alias]['version']) and self.__update_exists(alias):
                self.__stoplists[alias] = self.__update(alias)

        return self.__stoplists[alias]['terms']


    def __load(self, alias):

        files = [filename for filename in os.listdir(self.__datadir()) if alias in filename]

        if len(files) == 0:
            return None

        filename = files[0]

        version = filename.replace(alias + '_', '').replace('.json', '')

        if self.__is_outdated(version) and self.__update_exists(alias, version):
            return self.__update(alias, version)

        with open(self.__datadir() + filename) as file:
            terms = json.load(file)

        stoplist = {
            'alias': alias,
            'version': version,
            'terms': terms
        }

        return stoplist


    def __fetch(self, alias):

        response = requests.post(Stopwords.service_url + '/get', json={"name": alias}).json()

        stoplist = {
            'alias': alias,
            'version': response['version'],
            'terms': response['stopwords']
        }

        self.__store(stoplist)

        return stoplist


    def __update(self, alias, version):
        os.remove(self.__datadir() + alias + '_' + version + '.json')
        return self.__fetch(alias)


    def __store(self, stoplist):

        filename = stoplist['alias'] + '_' + stoplist['version'] + '.json'

        with open(self.__datadir() + filename, 'w', encoding='utf-8') as file:
            json.dump(stoplist['terms'], file, indent=4, ensure_ascii=False)


    def __update_exists(self, alias, version=None):

        if version is None:
            version = self.__stoplists[alias]['version']

        if int(version) < requests.post(Stopwords.service_url + '/version', json={"name": alias}).json():
            return True

        return False


    def __is_outdated(self, version):

        if self.__now_utc_timestamp() - int(version) > (Stopwords.version_TTL_hours * 60 * 60):
            return True

        return False


    def __datadir(self):
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), Stopwords.local_copy_dir + '/')


    def __now_utc_timestamp(self):
        return int(datetime.datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())

