import click

@click.command(name="city")
@click.option("--name", prompt="Enter city name", help="Name of the city to display")
def city(name):
    """
    Simple command to display the entered city name.
    """
    click.echo(f"The city you entered is: {name}")