import os
import json

from NDS.Repository.Stoplist import Stoplist




class FSStore:


    @staticmethod
    def load(alias):

        filename = FSStore.__find_file(alias)

        if filename is None:
            return None

        with open(FSStore.__datadir() + filename) as file:
            terms = json.load(file, encoding='utf8')

        stoplist = Stoplist(alias, terms, filename.replace(alias + '_', '').replace('.json', ''))

        return stoplist


    @staticmethod
    def store(stoplist):

        filename = stoplist.alias + '_' + stoplist.version + '.json'

        with open(FSStore.__datadir() + filename, 'w', encoding='utf-8') as file:
            json.dump(stoplist.terms, file, indent=4, ensure_ascii=False)


    @staticmethod
    def remove(alias):

        filename = FSStore.__find_file(alias)

        if filename is not None:
            os.remove(FSStore.__datadir() + filename)



    @staticmethod
    def __find_file(alias):

        files = [filename for filename in os.listdir(FSStore.__datadir()) if alias in filename]

        if len(files) == 0:
            return None

        return files[0]


    @staticmethod
    def __datadir():
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../repository/')

