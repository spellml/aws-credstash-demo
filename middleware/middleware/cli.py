import click
import subprocess
import os

@click.group()
def cli():
    pass

@click.command(name="connect", short_help="Shell out to psql.")
@click.option("-p", "--profile", help="Optional profile.", default="default")
def connect(profile):
    # get db address
    sp = subprocess.run(
        [
            "credstash", "--kms-region", "us-east-1", "--profile", profile,
            "get", "postgres_db_address"
        ],
        capture_output=True
    )
    if sp.returncode != 0:
        print("You do not have access to the database address!")
        return
    db_address = sp.stdout.decode('utf-8').rstrip()

    # get db password
    sp = subprocess.run(
        [
            "credstash", "--kms-region", "us-east-1", "--profile", profile,
            "get", "postgres_db_read_write_user_pwd"],
        capture_output=True
    )
    if sp.returncode != 0:
        print("You do not have access to the database password!")
        return
    db_pwd = sp.stdout.decode('utf-8').rstrip()

    connstr = f"postgresql://read_write:{db_pwd}@{db_address}:5432/postgres"

    # get psql executable path (required by os.execl)
    sp = subprocess.run(["which", "psql"], capture_output=True)
    if sp.returncode != 0:
        print("psql not installed, install that first.")
        return
    psql = sp.stdout.decode("utf-8").rstrip()

    os.execl(psql, psql, connstr)

cli.add_command(connect)
