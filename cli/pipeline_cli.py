from Pipeline import Pipeline
import click

CDAP_INSTANCE_URL = 'http://localhost:11015'

click.clear()


def progressBar(iterable):
    c = range(9999)
    with click.progressbar(c, label='exporting...') as bar:
        for i in bar:
            i=None


@click.group()
def piper():
    pass


@click.command()
@click.option('-u', '--cdap_instance', default=CDAP_INSTANCE_URL, help='CDAP instance to connect to.')
@click.option('-ns', '--namespace', default='default', help='Namespace to export from. If not specified, \
                                                            the default namespace will be used.')
@click.option('-t', '--type', default='app', help='Pipeline to export.  Default is to export all pipelines.')
@click.option('-o', '--output_dir', default='.', help='Directory to export the pipelines to.\
                                                        Default is the current directory.')
def export(cdap_instance, namespace, type, output_dir):
    ''' Export Pipelines '''
    click.echo(click.style('Export Pipeline(s)', fg='green', bold=True))
    click.echo('Namespace: %s \nPipeline(s): %s' % (namespace, type))
    p = Pipeline(cdap_instance)
    p.connect()
    # p.export(n='default', p='deployed', output_dir='~/my_pipelines')
    p.export(ns=namespace, p=type, output_dir=output_dir)
    # progressBar()


@click.command()
@click.option('-u', '--cdap_instance', default=CDAP_INSTANCE_URL, help='CDAP instance to connect to.')
def export_all(cdap_instance):
    ''' Export All Pipelines '''
    click.echo(click.style('Exporting All Pipeline(s)', fg='green', bold=True))
    p = Pipeline(cdap_instance)
    p.connect()
    p.export()
    # progressBar()


@click.command()
@click.option('-u', '--cdap_instance', default=CDAP_INSTANCE_URL, help='CDAP instance to connect to.')
def list(cdap_instance):
    ''' List all available Namespaces and Pipelines '''
    click.echo('List Pipelines')
    p = Pipeline(cdap_instance)
    p.connect()
    p.list()


@click.command()
@click.option('-u', '--cdap_instance', default=CDAP_INSTANCE_URL, help='CDAP instance to connect to.')
def status(cdap_instance):
    ''' Dispay the status of the CDAP instance '''
    click.echo('CDAP Status:')
    p = Pipeline(cdap_instance)
    p.connect()
    click.echo('Status:' + p.status)
    click.echo('Version:' + p.version)
    click.echo('Namespaces: {}'.format(p.namespaces))


piper.add_command(export)
piper.add_command(export_all)
piper.add_command(list)
piper.add_command(status)


if __name__ == '__main__':
    piper()
