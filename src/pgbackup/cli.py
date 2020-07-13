#!/bin/usr/python3


from argparse import Action, ArgumentParser

known_drivers = ['local', 's3']


class DriverAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        driver, destination = values
        if driver.lower() not in known_drivers:
            parser.error(
                "Unknown driver. Available drivers are 'local' and 's3'")

        namespace.driver = driver.lower()
        namespace.destination = destination


def create_parser():
    parser = ArgumentParser()
    parser.add_argument('url', help='URL of PostgreSQL database to backup')
    parser.add_argument('--driver', '-d',
                        nargs=2,
                        metavar=('driver', 'destination'),
                        required=True,
                        action=DriverAction,
                        help='how & where to store the backup')
    return parser


def main():
    import boto3
    import time
    from pgbackup import pgdump, storage

    args = create_parser().parse_args()
    dump = pgdump.dump(args.url)
    print(f"Got dump using url {args.url}")
    if args.driver == 's3':
        print(f"Uploading to s3\nBucket name {args.destination}")
        timestamp = time.strftime("%Y-%m-%dT%H%M%S", time.localtime())
        file_name = pgdump.dump_file_name(args.url, timestamp)
        client = boto3.client('s3')
        print(f"Created client; dump database to s3 as file name {file_name}")
        storage.s3(client, dump.stdout, args.destination, file_name)
        print(f"dumped  to s3")
    else:
        print(f"Uploading locally\nDestination file {args.destination}")
        outfile = open(args.destination, 'wb')
        print("opened destination file for writing")
        storage.local(dump.stdout, outfile)
        print(f"dumped database to destination file")
