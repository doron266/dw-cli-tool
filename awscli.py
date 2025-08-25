import click
import crud


@click.group(chain=True)
def cli() -> None:
    pass

cli.add_command(crud.s3)

cli.add_command(crud.ec2)

cli.add_command(crud.route53)

if __name__ == '__main__':
    cli()

