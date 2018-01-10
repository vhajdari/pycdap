import requests
import json
import os
import logging
from urlparse import urlparse
from datetime import datetime

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=__name__ + '.log',
                    filemode='w')

# write INFO messages or higher to the sys.stderr
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
sh.setFormatter(formatter)
# add the handler to the logger
log = logging.getLogger(__name__)
log.addHandler(sh)

class Colors:
    def __init__(self):
        pass

    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # '\n\x1b[1;31m' + 'Drafts:' + '\x1b[0m'


class Pipeline:
    __namespaces = '/v3/namespaces'
    __drafts = '/v3/configuration/user'
    __apps = '/apps'
    __status = '/status'
    __version = '/v3/version'
    __internal_types = ('_Tracker', 'dataprep')
    __artifact_type = 'cdap-data-pipeline'
    __port = 11015

    default_uri = 'http://localhost:11015'
    status = ''
    version = ''
    default_ns = 'default'
    namespaces = []
    output_dir = 'Pipelines'
    config = {'name': '', 'description': '', 'artifact': '', 'config': '', 'artifact_type': ''}

    def __init__(self, url=None):
        """
        Instantiates the Pipeline instance.

        Usage:
            Pipeline()                               - Use a local CDAP instance (localhost)
            Pipeline('http://localhost:11015')       - Same as Pipeline()
            Pipeline('http://hostname.domain:11015') - Use a specific CDAP instance.

        :param url:
        """
        self.url = url

    def connect(self):
        """
        Connect to CDAP instance and check its status.  Once connected, retrieve the version and available namespaces.
        :return:
        """
        if self.url:
            u = urlparse(self.url)
            if u.scheme not in ['http', 'https']:
                log.info('ERROR: Unknown protocol: {}'.format(u.scheme))
                return -1
            elif u.port != self.__port:
                log.info('ERROR: Unknown port: {}'.format(u.port))
                return -1
            elif u.path:
                log.info('ERROR: Unknown API endpoint: {}'.format(self.url))
                return -1
            else:
                self.__check_status()
                self.__get_namespaces()
        else:  # use default_uri
            log.info('Connected to CDAP instance: {}'.format(self.url))
            self.url = self.default_uri
            self.__check_status()
            self.__get_namespaces()

    def __check_status(self):
        """
        Check the status of the CDAP instance and set the appropriate class variables.

        :return: self.status, self.status
        """
        try:
            r = requests.get(self.url + self.__status)
            if r.text == 'OK':
                self.status = 'OK'
                # print self.status
                v = self.__get(self.url + self.__version)
                self.version = v['version']
            # print self.version
            return self.status, self.version
        except Exception as e:
            self.status = 'Connection error.'
            self.version = ''
            log.debug(self.status + '\n\t' + str(e))

    @staticmethod
    def __get(url):
        """
        Retrieve the JSON response from a given CDAP endpoint.

        :param url:
        :return:
        """
        r = None
        try:
            r = requests.get(url)
            if r.ok:
                d = r.json()
                return d
        except Exception as e:
            log.info('ERROR: ' + r.status_code + '\n\t' + str(e))

    def __save(self, data, pipeline_type, path=None):
        """
        Generate the exportable JSON for a pipeline and write it to disk

        :param data:
        :param pipeline_type:
        :return:
        """

        for i in data:
            ns = i.get('namespace')

            if pipeline_type == 'drafts':
                pipelines = i.get(pipeline_type)[0]
            elif pipeline_type == 'apps':
                pipelines = i.get(pipeline_type)
            else:
                log.info('ERROR.  Type can be either `apps` or drafts')
                return -1

            for p in pipelines:
                pipeline_name = p.get('pipeline_name')
                pipeline_config = json.loads(p.get('pipeline_json')).get('config')
                pc = json.dumps(pipeline_config, indent=True)
                self.__write(ns, pipeline_name + '-' + pipeline_type[:-1], pc, path)

    def __write(self, namespace, name, data, path=None):
        """
        Write the pipeline config out to a file.

        :param namespace:
        :param name:
        :param data:
        :return:
        """
        ts = datetime.now().strftime("%Y%m%d-%H.%M.%S")

        # log.debug('path argument = {}'.format(path))

        if not path:
            path = os.getcwd()
        else:
            path = os.path.expanduser(path)
            # log.debug('resolved path = {}'.format(path))

        file_name = name + '-' + self.version + '.json'
        directory = path + '/' + self.output_dir + '_' + ts + '/' + namespace
        file_path = directory + '/' + file_name

        # log.debug('File path = {}'.format(file_path))

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, 'w') as f:
            log.info('Saving Pipeline: {}'.format(file_path))
            f.write(data)

    def __get_namespaces(self):
        """
        Get the available namespaces for this CDAP instance.

        :return:
        """
        ns = []
        namespace_json = self.__get(self.url + self.__namespaces)
        for n in namespace_json:
            namespace_json = n.get('name')
            ns.append(namespace_json)
        self.namespaces = ns
        return

    def __check_namespaces(self, *ns):
        """
        Check the namespace arguments being passed in to make sure they exist on CDAP

        :param ns:
        :return: valid_namespaces
        """
        # if no arguments are provided then return all the available namespaces
        if not ns:
            log.debug('No arguments provided, returning all available namespaces: {}'.format(self.namespaces))
            return self.namespaces
        else:
            # Check if the provided namespace(s) exist
            # Check for duplicates. If there are duplicated we don't want to send them back.
            # If they are in the list return the valid selection, otherwise
            # terminate on the first encounter of an invalid namespace name
            valid_namespaces = []

            for i in set(ns):
                if i in self.namespaces:
                    # print '`{}` is valid'.format(i)
                    valid_namespaces.append(i)
                else:
                    log.info('This selection {} is not in the available namespaces. Terminating.'.format(ns))
                    exit(-1)

            # provided argument(s) is/are valid, return the valid_namespaces list:
            log.debug('The namespace selection {} is valid.'.format(valid_namespaces))
            return valid_namespaces

    # Get the draft pipelines -- this is NOT namespace specific
    # will retrieve the drafts in ALL namespaces
    def drafts(self, *namespaces):
        valid_ns = self.__check_namespaces(*namespaces)
        log.debug('drafts.valid_ns %s' % valid_ns)
        drafts_list = []
        drafts_json = self.__get(self.url + self.__drafts)

        # loop through all namespaces
        for namespace in valid_ns:
            # log.debug('Namespace: %s', namespace)
            # get all the drafts per namespace
            ns_drafts = {'namespace': namespace, 'drafts': []}
            pipelines = drafts_json.get('property').get('hydratorDrafts').get(namespace)
            draft_pipeline = []

            for k, v in pipelines.iteritems():
                name = v.get('name')
                self.config['name'] = name
                self.config['artifact'] = v.get('description')
                self.config['artifact'] = v.get('artifact')
                self.config['config'] = v.get('config')
                self.config['artifact_type'] = {'draft': {'id': k}}
                pipeline_json = json.dumps(self.config)
                draft_pipeline.append({
                    'pipeline_name': name,
                    'pipeline_json': pipeline_json
                })

            ns_drafts['drafts'].append(draft_pipeline)
            drafts_list.append(ns_drafts)

        # print json.dumps(drafts, sort_keys=True, indent=4)
        # return json.dumps(drafts, indent=4)
        return drafts_list

    def apps(self, *namespaces):
        """
        Retrieve all apps deployed apps for all namespaces or any given namespace

        Example of an App collection endpoint:
         http://localhost:11015/v3/namespaces/default/apps

        :param namespaces:
        :return:
        """
        log.debug('Retrieving apps for namespace: {}'.format(namespaces))
        valid_ns = self.__check_namespaces(*namespaces)
        apps_list = []
        for namespace in valid_ns:
            pipelines = []
            apps_json = self.__get(self.url + self.__namespaces + '/' + namespace + self.__apps)
            # get the deployed pipelines in this namespace
            for i in apps_json:
                # filter out anything other than cdap-data-pipeline
                artifact_type = i.get('artifact').get('name')
                if self.__artifact_type == artifact_type:
                    app_id = i['id']
                    if app_id not in self.__internal_types:
                        # log.debug('App Namespace: %s', ns)
                        # log.debug('pipeline name: %s', id)
                        app = self.__get_app_config(namespace, app_id)
                        # log.debug('Pipeline = %s', json.dumps(app, sort_keys=True, indent=4))
                        name = app.get('name')
                        self.config['name'] = name
                        self.config['description'] = app.get('description')
                        self.config['artifact'] = app.get('artifact')
                        self.config['artifact_type'] = 'deployed'
                        self.config['config'] = json.loads(app.get('configuration'))

                        pipeline_json = json.dumps(self.config)
                        pipelines.append({
                            'pipeline_name': name,
                            'pipeline_json': pipeline_json
                        })
            apps_list.append({'namespace': namespace, 'apps': pipelines})
        return apps_list

    def __get_app_config(self, namespace, app_name):
        """
        Get the json data for a single app

        Example of an individual App endpoint:
         http://localhost:11015/v3/namespaces/default/apps/MyAppName

        :param namespace:
        :param app_name:
        :return:
        """
        log.debug('Retrieving configuration for deployed pipeline: {}'.format(app_name))
        return self.__get(self.url + self.__namespaces + '/' + namespace + self.__apps + '/' + app_name)

    def list(self):
        """
        Print out a listing of all the namespaces and the pipelines contained within

        :return:
        """
        log.debug('Printing out a listing of all the namespaces and pipelines')
        namespaces = self.namespaces
        namespaces.sort()
        print Colors.GREEN + Colors.BOLD + 'Namespaces: ({})'.format(namespaces.__len__()) + Colors.ENDC
        for i in namespaces:
            n = namespaces.index(i) + 1
            print '\t{} - {}'.format(n, i)

        print Colors.RED + Colors.BOLD + 'Drafts:' + Colors.ENDC
        drafts = self.drafts()
        for pipelines in drafts:
            print '   Namespace: {}'.format(pipelines['namespace'])
            pipeline = pipelines['drafts'][0]

            for name in pipeline:
                n = pipeline.index(name) + 1
                print '     {} - {}'.format(n, name['pipeline_name'])

        print Colors.BLUE + Colors.BOLD + 'Apps:' + Colors.ENDC
        apps = self.apps()
        for pipelines in apps:
            print '   Namespace: {}'.format(pipelines['namespace'])
            pipeline = pipelines['apps']

            for name in pipeline:
                n = pipeline.index(name) + 1
                print '     {} - {}'.format(n, name.get('pipeline_name'))

        pass

    def export(self, **kwargs):
        """
        Export pipelines using one of the following signatures.

        Usage:
            Pipeline.export()                       - Exports all pipelines in all namespaces
            Pipeline.export(namespace='NS1')        - Exports all pipelines for namespace NS1
            Pipeline.export(n='NS1', p='app')       - Exports all the deployed pipelines for namespace NS1
            Pipeline.export(ns='NS1', type='draft') - Exports all the draft pipelines for namespace NS1

            You can use the following aliases (short hand) for the keys:
                namespace: n, ns, namespace
                pipelines: p, pipeline, pipelines, type

                    The pipeline type can be one of the following values:
                        app, apps, deployed, draft, drafts

        :param kwargs: namespace_name, pipeline_type
        :return:
        """
        log.debug('Exporting pipelines: {}'.format(kwargs))
        if not kwargs:  # no arguments given
            log.info('Exporting all pipelines in all namespaces.')
            drafts = self.drafts()
            apps = self.apps()
            self.__save(drafts, 'drafts')
            self.__save(apps, 'apps')
            return 0

        if kwargs.__len__() > 3:
            log.info('Error: Maximum of 3 parameters allowed.\n\t'
                     'Ex. Pipelines.export(namespace="default", pipelines="draft", \
                      output_dir="/home/user") ')
            exit(-1)

        if kwargs.__len__() <= 3:
            namespace_alias = ('n', 'ns', 'namespace')
            pipeline_alias = ('p', 'pipeline', 'pipelines', 'type')
            pipeline_apps_alias = ('app', 'apps', 'deployed')
            pipeline_drafts_alias = ('draft', 'drafts')
            pipeline_all_types = ('all', '*')
            pipeline_type_alias = pipeline_apps_alias + pipeline_drafts_alias + pipeline_all_types
            output_dir = ('o', 'output_dir')
            nsk = None
            pk = None
            nsv = None
            pv = None
            dir = None

            for k, v in kwargs.iteritems():
                log.debug('argument = {}'.format(k))
                if k not in (namespace_alias + pipeline_alias + output_dir):
                    log.info('ERROR. Invalid parameter `{}`'.format(k))
                    exit(-1)
                if k in namespace_alias:
                    nsk = k
                    nsv = v
                if k in pipeline_alias:
                    pk = k
                    pv = v
                    if pv not in pipeline_type_alias:
                        log.info('ERROR. Invalid argument `{}`'.format(pv))
                        exit(-1)
                # if the output directory is specified use that,
                # otherwise use the current working directory
                if k in output_dir:
                    dir = v
                else:
                    dir = os.getcwd()

            log.debug('pipeline arguments: {} = {}, {} = {}'.format(nsk, nsv, pk, pv))
            log.debug('dir argument = {}'.format(dir))

            # export: namespace signature
            if nsk and not pk:
                log.debug('Exporting using the namespace signature')
                drafts = self.drafts(nsv)
                apps = self.apps(nsv)
                self.__save(drafts, 'drafts', dir)
                self.__save(apps, 'apps', dir)

            # export: namespace  + pipeline signature
            elif nsk and pk:
                log.debug('Exporting using the namespace  + pipeline signature')
                if pv == 'all':
                    drafts = self.drafts(nsv)
                    apps = self.apps(nsv)
                    self.__save(drafts, 'drafts', dir)
                    self.__save(apps, 'apps', dir)
                if pv in pipeline_apps_alias:
                    apps = self.apps(nsv)
                    self.__save(apps, 'apps', dir)
                if pv in pipeline_drafts_alias:
                    drafts = self.drafts(nsv)
                    self.__save(drafts, 'drafts', dir)
            else:
                pass