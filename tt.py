#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from flask import Flask
from flask_restplus import Api, Resource, fields

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
# 工厂模式注册API
api = Api(app, version='1.0', title='TodoMVC API',
    description='中文接口模拟测试',
)

ns = api.namespace('todos', description='TODO operations')

# 配置 描述响应的结构
todo = api.model('Todo', {
    'id': fields.Integer(readOnly=True, description='测试中文接口'),
    'task': fields.String(required=True, description='The task details')
})


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('列出资源')
    @ns.marshal_list_with(todo)
    def get(self):
        '''列出所有的任务'''
        return DAO.todos

    @ns.doc('创建资源')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''创建一个新的任务'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resourceAAA哈哈哈'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)