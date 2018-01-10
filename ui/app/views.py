from app import app
from flask import render_template, redirect, request, make_response, jsonify
from pycdap import Pipeline
import json
import logging

# TODO: Change to RotatingLogHandler
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

#
# try:
#    #connect to CDAP
#    p = Pipeline('http://localhost:11015')
#    p.connect()
#    print "Connected successfully!!!"
# except Exception, e:
#    print "Could not connect to CDAP: %s" % e

p = Pipeline('http://localhost:11015')
p.connect()
print "Connected to CDAP!!!"


@app.route('/', methods=['GET'])
@app.route('/list', methods=['GET'])
def list():
    # pipelines = p.list('json')
    apps = p.apps()
    # apps.sort()
    drafts = p.drafts()
    # drafts.sort()
    return render_template('list.html', apps=apps, drafts=drafts)


@app.route('/export', methods=['GET'])
def export():
    return render_template('export.html')


@app.route('/export/<pipeline_name>', methods=['POST'])
def export_pipeline(pipeline_name):
    return render_template('export_pipeline.html')

####################################################################################################################


# namespaces = p.namespaces

# data = {}
#
# for i in data:
#     ns = i.get('namespace')
#
#     if pipeline_type in ('drafts', 'apps'):
#         pipelines = i.get(pipeline_type)
#     else:
#         log.info('ERROR.  Type can be either `apps` or drafts')
#         return -1
#
#     for p in pipelines:
#         pipeline_name = p.get('pipeline_name')
#         pipeline_config = json.loads(p.get('pipeline_json')).get('config')
#         pc = json.dumps(pipeline_config, indent=True)
#         self.__write(ns, pipeline_name + '-' + pipeline_type[:-1], pc, path)

# drafts = p.drafts()
# for pipelines in drafts:
#     ns = pipelines['namespace']
#     pipeline = pipelines['drafts'][0]
#     for name in pipeline:
#         pipeline_name = name['pipeline_name']
#         pipelines.update({'namespace': ns, 'pipeline_name': pipeline_name})

# apps = p.apps()
# for pipelines in apps:
#     ns = pipelines['namespace']
#     pipeline = pipelines['apps']
#     for name in pipeline:
#         pipeline_name = name['pipeline_name']
#         pipelines.update({'namespace': ns, 'pipeline_name': pipeline_name})
