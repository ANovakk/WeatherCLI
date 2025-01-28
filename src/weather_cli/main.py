import click
from weather_cli.commands.city import city
from weather_cli.commands.now import now

@click.group()
def main():
    "Weather CLI Application"
    pass

main.add_command(city)
main.add_command(now)