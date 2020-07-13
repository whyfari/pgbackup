import pytest
import subprocess

from pgbackup import pgdump


url = "posgres://bob@example.com:5432/db_one"


def test_dump_calls_pg_dump(mocker):
    """
    Utilize pg_dump with the database URL
    """
    # we use Popen instead or subprocess because we want it to happen in the background

    # patching using mock allows us to substitute the implementation of something with something else we can use and call assertions on and prevent it from doing other things the normal implementation would have
    # after this point anytime the subprocess.Popen function is called; it behaves differently; it's being mocked
    # basically we make it into a function that can take any arguments it wants and it's gonna store the number of time this function is called
    mocker.patch('subprocess.Popen')

    assert pgdump.dump(url)
    subprocess.Popen.assert_called_with(
        ['pg_dump', url], stdout=subprocess.PIPE)


def test_dump_handles_oserror(mocker):
    """
    pgdump.dump return sa reasonable error if pg_dump isn't isntalled
    """

    mocker.patch('subprocess.Popen', side_effect=OSError('no such file'))
    with pytest.raises(SystemExit):
        pgdump.dump(url)


def test_dump_file_name_without_timestamp():
    """
    pgdump.dump_dump_file_name returns the name of the database
    """
    assert pgdump.dump_file_name(url) == 'db_one.sql'


def test_dump_file_name_with_timestamp():
    """
    pgdump.dump_dump_file_name returns the name of the database with timestamp
    """
    timestamp = '2020-07-12T13:14:10'
    assert pgdump.dump_file_name(url, timestamp) == f'db_one-{timestamp}.sql'
