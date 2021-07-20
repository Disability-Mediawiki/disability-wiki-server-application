

import csv
import json
import logging
import os
import time
import pandas as pd
from application.main.service.AuthenticationService import (
    token_authenticate, token_authenticate_admin, get_user_by_auth)
from application.main.service.FileService import FileService
from application.main.service.PdfService import PdfService
from flask import (Flask, current_app, jsonify, make_response, request,
                   send_file, send_from_directory)
from flask_cors import cross_origin
from flask_restful import Resource, reqparse
from flask_restplus import Api, Namespace, Resource
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from celery import Celery
from time import sleep
from application.main.service.AsyncTask import task
from application.main.service.AsynTask2 import printtest
from application.main.service.AsyncService import AsyncService
from application.main.service.AsyncTask3 import print_numbers, print_task
from redis import Redis
from rq import Queue, Connection, Worker
from rq.job import Job
from datetime import datetime, timedelta

import pika

api = Namespace('REDIS_CONTROLLER', description='Redis test operations')


# celery = Celery('AsyncTask', broker='localhost:6379')


@api.route('/test-async', methods=['GET'])
class AsyncTest(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.file_service = PdfService()
        self.broker_url = 'redis://localhost:6380'
        super(AsyncTest, self).__init__(*args, **kwargs)

    # @celery.task(bind=True)
    # def some_long_task(self):
    #     sleep(5)
    #     print('LKASJDLKASJD')

    def get(self):
        print("got connection")
        # self.some_long_task.delay()
        # task.apply_async()
        task.delay()
        return "ok"

# CURRENTLY WORKING
# TYPE RQ to START THE QUEUE WORKER
# https://www.twilio.com/blog/asynchronous-tasks-in-python-with-redis-queue


@api.route('/test-async2', methods=['GET'])
class AsyncTest2(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.q = Queue(connection=Redis())

        # CREATE WORKER

        super(AsyncTest2, self).__init__(*args, **kwargs)

    def get(self):
        print("got connection")
        # self.some_long_task.delay()
        # task.apply_async()

        result = self.q.enqueue(printtest, 'http://nvie.com')
        return result.id


@api.route('/test-async3', methods=['GET'])
class AsyncTest3(Resource):

    def __init__(self, *args, **kwargs):
        redis_conn = Redis(
            host=os.getenv("REDIS_HOST", "127.0.0.1"),
            port=os.getenv("REDIS_PORT", "6379"),
            password=os.getenv("REDIS_PASSWORD", ""),
        )

        self.redis_queue = Queue(connection=redis_conn)

        # self.queue = Queue(connection=Redis())
        super(AsyncTest3, self).__init__(*args, **kwargs)

    def print_numbers(self):
        print("Starting num task")
        for num in range(3):
            print(num)
            time.sleep(1)
        print("Task to print_numbers completed")
        return "TEST TEXT FROM REDDIS"
    # def queue_tasks(self):
    #     self.queue.enqueue(print_task, 5)
    #     self.queue.enqueue_in(timedelta(seconds=10), print_numbers, 5)

    def get(self):
        # self.queue_tasks()
        job = self.redis_queue.enqueue(self.print_numbers)
        return jsonify({"job_id": job.id})


@api.route('/test-celery', methods=['GET'])
class CeleryTest(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        # self.q = Queue(connection=Redis())

        self.async_service = AsyncService()

        # CREATE WORKER

        super(CeleryTest, self).__init__(*args, **kwargs)

    def get(self):
        print("got connection")
        # d = task.apply_async(23, 42)
        # d.wait()
        # d = task.apply_async()
        self.async_service.task.apply_async()
        # result = self.q.enqueue(printtest, 'http://nvie.com')
        return "OK"


@api.route("/check_status")
class check_status(Resource):
    def __init__(self, *args, **kwargs):
        self.redis_conn = Redis(
            host=os.getenv("REDIS_HOST", "127.0.0.1"),
            port=os.getenv("REDIS_PORT", "6379"),
            password=os.getenv("REDIS_PASSWORD", ""),
        )
        self.redis_queue = Queue(connection=self.redis_conn)

        # self.queue = Queue(connection=Redis())
        super(check_status, self).__init__(*args, **kwargs)

    parser = None
    parser = api.parser()
    parser.add_argument('job_id', type=str, help='File job_id')

    @api.doc(parser=parser, validate=True)
    def get(self):
        """Takes a job_id and checks its status in redis queue."""
        job_id = request.args["job_id"]

        try:
            job = Job.fetch(job_id, connection=self.redis_conn)
        except Exception as exception:
            return exception

        return jsonify({"job_id": job.id, "job_status": job.get_status(), "jobs_status": job.result})


@api.route("/get_results")
class get_results(Resource):
    def __init__(self, *args, **kwargs):
        self.redis_conn = Redis(
            host=os.getenv("REDIS_HOST", "127.0.0.1"),
            port=os.getenv("REDIS_PORT", "6379"),
            password=os.getenv("REDIS_PASSWORD", ""),
        )
        self.redis_queue = Queue(connection=self.redis_conn)

        # self.queue = Queue(connection=Redis())
        super(get_results, self).__init__(*args, **kwargs)

    parser = None
    parser = api.parser()
    parser.add_argument('job_id', type=str, help='File job_id')

    @api.doc(parser=parser, validate=True)
    def get(self):
        """Takes a job_id and checks its status in redis queue."""
        job_id = request.args["job_id"]

        try:
            job = Job.fetch(job_id, connection=self.redis_conn)
        except Exception as exception:
            return exception

        return jsonify({"jobs_status": job.result})


@api.route('/rabbit-mq', methods=['GET'])
class RabbitTest(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("text", type=str,
                                 help='text', required=True)
        super(RabbitTest, self).__init__(*args, **kwargs)

    parser = None
    parser = api.parser()
    parser.add_argument('text', type=str, help='text enter')

    @api.doc(parser=parser, validate=True)
    def get(self):
        args = self.parser.parse_args(strict=True)
        cmd = args.get('text')
        # connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='rabbitmq'))
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=cmd,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        connection.close()
        return " [x] Sent: %s" % cmd


@api.route('/rabbit-mq2', methods=['GET'])
class RabbitTest2(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("text", type=str,
                                 help='text', required=True)
        super(RabbitTest2, self).__init__(*args, **kwargs)

    parser = None
    parser = api.parser()
    parser.add_argument('text', type=str, help='text enter')

    @api.doc(parser=parser, validate=True)
    def get(self):
        args = self.parser.parse_args(strict=True)
        cmd = json.dumps({'data': args.get('text')})
        # connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='rabbitmq'))
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='doc_classify_queue', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='doc_classify_queue',
            body=cmd,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        connection.close()
        return " [x] Sent: %s" % cmd
