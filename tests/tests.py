from pycdap import Pipeline
import json


p = Pipeline('http://Vetons-MBP.home:11015')
p.connect()
print '\n====================================='
print 'url: {}'.format(p.url)
# print 'default_uri: {}'.format(p.default_uri)
print 'status: {}'.format(p.status)
print 'version: {}'.format(p.version)
print 'namespaces: {}'.format(p.namespaces)
print '=====================================\n'

# print dir(p)
# print p._Pipeline__check_namespaces('default', 'PRGX')
# p.export(ns='all', pipelines='draft')

# === LIST ===
# p.list()
# print json.dumps(p.list('json'), indent=2, sort_keys=True)

# === APPS ===
#apps = c.apps()
# print json.dumps(p.apps(), indent=2)                  # return all apps in the all ns
# print json.dumps(p.apps('default'), indent=2)         # return all apps in the 'default' ns
# print json.dumps(p.apps('default', 'PRGX'), indent=2) # return all apps in the 'default' and 'PRGX' ns
# print json.dumps(p.apps('foo'), indent=2)             # Terminate, 'foo' is not a valid namespace
# print json.dumps(p.apps('foo', 'default'), indent=2)  # Terminate: even though 'default is valid 'foo' is not


# === DRAFTS ===
# print json.dumps(p.drafts(), indent=2)                # return all drafts in all ns
# print json.dumps(p.drafts('default'), indent=2)         # return all drafts in 'default' ns
# print json.dumps(p.drafts('default', 'PRGX'), indent=2) # return all drafts in 'default' ns
# print json.dumps(p.drafts('foo'), indent=2)               # Terminate, 'foo' is not a valid namespace
# print json.dumps(p.drafts('default', 'foo'), indent=2)   # Terminate: even though 'default is valid 'foo' is not
# print json.dumps(p.drafts('default','default','default'), indent=2)         # return all drafts in 'default' ns

# === EXPORT ===
# namespaces = 'n', 'ns', 'namespace'
# types = 'p', 'pipeline', 'pipelines', 'type'
# app types: ('app', 'apps', 'deployed')
# draft types: ('draft', 'drafts')
# p.export()                            # Exports all pipelines in all namespaces
# p.export(namespace='NS1')         # Exports all pipelines for namespace NS1
# p.export(n='default', p='app')       # Exports all the deployed pipelines for namespace NS1
# p.export(ns='default', type='app')    # Exports all the draft pipelines for namespace NS1
#
# p.export(ns='default', type='all')
# p.export(ns='default', type='all', o='.')
# p.export(ns='default', type='app', o='/tmp')

