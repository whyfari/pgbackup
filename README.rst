pgbackup
========

CLI for backiup remote PostgresSQL datbase either locally or to S3

Preparing for Development
-------------------------

1. Ensure ``pip`` and ``pipenv`` are installed
2. Clonse repository: ``git clone git@github.com:whyfari/pgbackup``
3. ``cd`` into repository.
4. Fetch development dependencies ``make install``
5. Activate virtualenv: ``pipenv shell``

Usage
-----

Pass in a full database URL, the storage driver, and the destination

S3 Example w/ bucket name:

::

    $ pgbackup posgres://bob@example.com:5432/db_one --driver s3 backups

Local Example w/ local name:

::

    $ pgbackup posgres://bob@example.com:5432/db_one --driver local /var/local/db_one/backups/dump.sql 


Running Tests
-------------

Run tests locally using ``make`` if virtualenv is active:

::

    $ make

if virtual env isn't active then use:

::

   $ pipenv run make
