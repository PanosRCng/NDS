import datetime
from datetime import timezone
from time import sleep

from Core.Config import Config
from Core.Logger import Logger
from NDS.Repository.Repository import Repository



class Updater:


    @staticmethod
    def update():

        while True:

            for alias in Config.get('nds')['stopwords']:

                Updater.__check_update(alias)

                sleep((Config.get('nds')['updater']['check_update_interval_hours'] * 60 * 60))



    @staticmethod
    def __check_update(alias):

        current_version = Repository.version(alias)

        if Updater.__is_outdated(current_version) is False:
            return

        Logger.log(__name__, 'current version ' + current_version + ' for ' + alias + ' is expired due to age, requesting new...')
        Repository.update(alias)


    @staticmethod
    def __is_outdated(current_version):

        if Updater.__now_utc_timestamp() - int(current_version) > (Config.get('nds')['updater']['version_TTL_hours'] * 60 * 60):
            return True

        return False


    @staticmethod
    def __now_utc_timestamp():
        return int(datetime.datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())


