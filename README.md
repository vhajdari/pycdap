# pycdap
Python library and CLI for exporting CDAP Pipelines

If you want use the **pycdap** library in your own python projects simply import the 
Pipeline module and configure an object instance.

There is also a command line interface (CLI) bundled with this library that lets you 
use the Pipeline module from the command line for interacting with your CDAP instance.

## Setup
To install pycdap run the setup.py installer from within the pycdap directory. 
The installer will create an executable named **piper**.
```bash
pip install .
-- or --
python setup.py install
```

**piper** allows you to interact with your CDAP instance via the console.

## CLI Usage
To list the available sub-commands for **piper** use the `--help` argument.  
Each sub command has usage information available.
``` commandline
piper --help
piper export --help 
``` 
### List Pipelines
Print out a listing of all the available namespaces and pipelines contained within.
``` commandline
piper list
``` 
### Status of CDAP Instance
To get the version, status and the namespaces available on a CDAP instance, execute:
``` commandline
piper status
-- or --
piper status -u http://10.30.20.123:11015 
``` 
### Export Pipelines
There are two export options available ` export ` and ` export_all `.  
The former option takes key/word arguments, whereas the later exports all 
namespaces and all the pipelines per namespace.
``` commandline
piper export -ns default -t draft -o /tmp/my_pipelines
piper export -u http://10.30.20.123:11015 
``` 
#### Arguments and Options
**export**:
* -u, --cdap_instance ... CDAP instance to connect to. Defaults to `http://localhost:11015`
* -ns, --namespace ...... Namespace to export from. If not specified, the `default` namespace will be used.
* -t, --type .................... Pipeline to export.  Default is to export all pipelines.
* -o', --output_dir ......... Directory to export the pipelines to. Defaults to the current directory.

**export_all**:
* -u, --cdap_instance ... CDAP instance to connect to. Defaults to `http://localhost:11015`

#### Usage Examples:
```bash
piper export -ns NS1                              #export all pipeline types from the `NS1` namespace 
piper export -u http://10.30.20.123:11015 -t all  #export all pipeline types from the `default` namespace on a remote CDAP instance.
piper export -ns NS1 -t drafts -o ~/cdap/drafts   #export draft pipeline from the `NS1 namespace and write output to /home/username/cdap/drafts
#
piper export_all                                  #export all pipeline from all namespaces 
piper export_all -u http://10.30.20.123:11015     #export all pipeline from all namespaces on a remote CDAP instance.
```



## Library Usage:
```python
import Pipeline
p = Pipeline('http://localhost:11015')
p.connect()
p.list()
```

### LIST
Prints out a listing of all the pipelines 

```python
p.list()
```

### APPS = Deployed Pipelines
```python
apps = c.apps()
print json.dumps(p.apps(), indent=2)                  # return all apps in the all namespaces
print json.dumps(p.apps('default'), indent=2)         # return all apps in the 'default' ns
print json.dumps(p.apps('default', 'NS1'), indent=2)  # return all apps in the 'default' and 'NS1' ns
print json.dumps(p.apps('foo'), indent=2)             # Terminate, 'foo' is not a valid namespace
print json.dumps(p.apps('foo', 'default'), indent=2)  # Terminate: even though 'default is valid 'foo' is not

```

### DRAFTS - Draft Pipelines
```python
print json.dumps(p.drafts(), indent=2)                  # return all drafts in all ns
print json.dumps(p.drafts('default'), indent=2)         # return all drafts in 'default' ns
print json.dumps(p.drafts('default', 'NS1'), indent=2)  # return all drafts in 'default' ns
print json.dumps(p.drafts('foo'), indent=2)             # Terminate, 'foo' is not a valid namespace
print json.dumps(p.drafts('default', 'foo'), indent=2)  # Terminate: even though 'default is valid 'foo' is not
print json.dumps(p.drafts('default','default','default'), indent=2)         # return all drafts in 'default' ns

```

### EXPORT - Save Pipelines Configs to Disk
Unless specified, all pipelines will be saved to the current working directory where **piper** is executed from.
```python
### Parameter options ###
# namespaces = 'n', 'ns', 'namespace'
# pipeline types = 'p', 'pipeline', 'pipelines', 'type'
# app types: 'app', 'apps', 'deployed'
# draft types: 'draft', 'drafts'
.
p.export()                                      # Exports all pipelines in all namespaces
p.export(namespace='NS1')                       # Exports all pipelines in namespace `NS1`
p.export(ns='NS1', type='all')                  # Exports all pipelines in namespace `NS1` -- same as above
p.export(n='default', p='app')                  # Exports deployed pipelines for namespace `default`
p.export(ns='default', type='draft')            # Exports draft pipelines for namespace `default`
p.export(ns='NS1', type='all', o='.')           # Exports all pipelines in namespace `NS1`, and save them to current directory
p.export(ns='NS1', type='deployed', o='/tmp')   # Exports draft pipelines in namespace `NS1` and save them to /tmp
```

