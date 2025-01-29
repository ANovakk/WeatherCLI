import click
from weather_cli.commands.now import now

@click.group()
def main():
    "Weather CLI Application"
    pass

main.add_command(now)