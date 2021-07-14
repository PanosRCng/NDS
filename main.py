import argparse




def main():

    parser = argparse.ArgumentParser("main.py", description='Negative Dictionary System')
    subparsers = parser.add_subparsers(help='operations', dest='operation')

    start_system_parser = subparsers.add_parser('start', help='starts the system (server, updater, feeders)')
    start_system_parser.add_argument('-no_feeders', dest='no_feeders', action='store_true', help='start the system without the feeders')
    start_system_parser.set_defaults(no_feeders=False)

    start_feeder_parser = subparsers.add_parser('start_feeder', help='starts a specific feeder')
    start_feeder_parser.add_argument('alias', metavar='alias', type=str, help='the feeder alias')


    args = vars(parser.parse_args())

    if args['operation'] == 'start':
        import nds
        nds.start(args['no_feeders'])

    if args['operation'] == 'start_feeder':
        from NDS.Feeder import Feeder
        Feeder.feed(args['alias'])





if __name__ == '__main__':
    main()
