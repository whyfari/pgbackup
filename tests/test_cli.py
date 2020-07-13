#!/bin/usr/python3

import pytest
from pgbackup import cli

# Doing TDD - Test driven
# READ > Green > Refactor

#    pgbackup posgres://bob@example.com:5432/db_one --driver s3 backups

url = "posgres://bob@example.com:5432/db_one"


@pytest.fixture
def parser():
    return cli.create_parser()


def test_parser_without_driver(parser):
    """
    Without a specified driver the parser will exit
    """
    with pytest.raises(SystemExit):
        parser.parse_args([url])


def test_parse_with_unknown_driver(parser):
    """
    The parser will exist if the driver name is unknown.
    """
    with pytest.raises(SystemExit):
        parser.parse_args([url, '--driver', 'azure', 'destination'])


def test_parse_with_known_driver(parser):
    """
    The parser will exist if the driver name is unknown.
    """
    for driver in ['local', 's3']:
        assert parser.parse_args([url, '--driver', driver, 'destination'])


def test_parser_withDriver(parser):
    """
    The parser will exit if it receives a driver w/o a destination
    """
    with pytest.raises(SystemExit):
        parser.parse_args([url, "--driver", "local"])


def test_parser_with_driver_and_destination():
    """
    Parser will not exit if it receives a driver and a destination
    """
    parser = cli.create_parser()
    args = parser.parse_args([url, '--driver', 'local', '/some/path'])

    assert args.url == url
    assert args.driver == 'local'
    assert args.destination == '/some/path'
