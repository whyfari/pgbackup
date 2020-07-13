from pgbackup import storage
import tempfile
import pytest


@pytest.fixture
def infile():
    f = tempfile.TemporaryFile()
    f.write(b'Testing')
    f.seek(0)
    return f


def test_storing_file_locally(infile):
    """
    Writes content from one file-like to another
    """

    outfile = tempfile.NamedTemporaryFile(delete=False)
    storage.local(infile, outfile)
    with open(outfile.name, 'rb') as f:
        assert f.read() == b'Testing'


def test_storing_file_on_s3(mocker, infile):
    """
    writes content from one file-like to s3
    """

    # duct-typing; only real requirement is that the client object it receives adheres to a certain method signature (it has an upload_fileobj method)

    # we mock the client object
    client = mocker.Mock()

    # ideal usage
    storage.s3(client, infile, "bucket", "file-name")

    client.upload_fileobj.assert_called_with(infile, "bucket", "file-name")
