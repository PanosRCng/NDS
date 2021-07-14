import os
import signal
from multiprocessing import Process
from threading import Thread
import json

from flask import Flask, request, abort

from Core.Config import Config
from NDS.Repository.Repository import Repository
from NDS.Updater import Updater
from NDS.Feeder import Feeder



server = Flask(__name__)




@server.route('/list', methods=['GET'])
def list_route():
    return handle_list_request()


@server.route('/version', methods=['POST'])
def version_route():

    try:

        req = request.get_json()

        alias = req['name']

    except Exception as ex:
        abort(400)

    return handle_version_request(alias)


@server.route('/get', methods=['POST'])
def stopwords_route():

    try:

        req = request.get_json()

        alias = req['name']

    except Exception as ex:
        abort(400)

    return handle_get_request(alias)


def handle_list_request():
    return json.dumps(Repository.list())


def handle_version_request(alias):
    return Repository.version(alias)


def handle_get_request(alias):
    return json.dumps({'version': Repository.version(alias), 'stopwords': Repository.get(alias)}, indent=4, ensure_ascii=False)



def signal_exit_handler(sig, frame):
    os._exit(1)


def feeder_processes(stopwords_config):
    return [Process(target=Feeder.feed, args=[alias]) for alias in stopwords_config if stopwords_config[alias]['feed_enabled'] is True]




def start(no_feeders=False):

    signal.signal(signal.SIGINT, signal_exit_handler)

    server_config = Config.get('server')
    nds_config = Config.get('nds')

    updater_thread = Thread(target=Updater.update)

    if no_feeders is False:
        feeder_procs = feeder_processes(nds_config['stopwords'])
        for proc in feeder_procs:
            proc.start()

    updater_thread.start()


    server.run(host=server_config['host'], port=server_config['port'], threaded=True)


    updater_thread.join()

    if no_feeders is False:
        for proc in feeder_procs:
            proc.join()


