import click
from commands.city import city_command

@click.group()
def main():
    "Weather CLI Application"
    pass

main.add_command(city_command)

if __name__ == "__main__":
    main()