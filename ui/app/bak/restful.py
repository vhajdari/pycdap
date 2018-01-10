all()from app import app
from flask import render_template, redirect, request, make_response, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

#import hunnydo

try:
	#location of the db instance assumes default port
	client = MongoClient('mongodb://172.16.241.10')
	print "Connected successfully!!!"
	db = client.hunnydo
	hdl = db.dolist
except pymongo.errors.ConnectionFailure, e:
  	print "Could not connect to MongoDB: %s" % e 


@app.route('/', methods=['GET'])
@app.route('/list', methods=['GET'])
def honeydo():
   tasks = list(hdl.find())
   return render_template('list.html', tasks=tasks, count=len(tasks))  

@app.route('/do', methods=['POST'])
def domore():
   task = request.form.get('task')
   hdl.insert({'task' : task, 'status':'new', 'date':datetime.datetime.utcnow()})
   return redirect('/')


@app.route('/tasks', methods=['GET'])
def json():
   tasks = hdl.find()
   res = []
   for task in tasks:
      d = {}
      d['id'] = str(task['_id'])
      d['task'] = task['task']
      d['status'] = task['status']
      d['date'] = str(task['date'])
      res.append(d)
   print 'json = ', res
   return jsonify({'tasks': res})

@app.route('/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def tasks(task_id):
   if len(task_id) == 0:
      abort(404) 

   if request.method == 'GET':
      task = hdl.find_one({'_id': ObjectId(task_id)})
      print "Get task. task_id = ", task_id
      d = {}
      d['task'] = task['task']
      d['status'] = task['status']
      d['date'] = str(task['date'])
      return jsonify(d)

   if request.method == 'PUT':
      task = hdl.find_one({'_id': ObjectId(task_id)})
      print "Task completed. task_id = ", task_id
      if task_id == str(task['_id']):
         result = hdl.update(
            {"_id":ObjectId(task_id)}, {"$set": {"status":"done"}}, upsert = False
         )
         print result
      return redirect('/')

   if request.method == 'DELETE':
      print "Deleting record. task_id = ", task_id
      result = hdl.remove({'_id': ObjectId(task_id)})
      print result
      return redirect('/')

@app.route('/delete/<task_id>', methods=['POST'])
def delete(task_id):
   hdl.remove({'_id': ObjectId(task_id)})
   return redirect('/')