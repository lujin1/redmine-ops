from flask import Blueprint, Response, request
import json
from flask_apscheduler import APScheduler
from api.redmine import *

class Config(object):
    SCHEDULER_API_ENABLED = True
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 10}
    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 3
    }

app.logger.setLevel(logging.INFO)
app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)

job_api = Blueprint('job_api', __name__, url_prefix = '/job')

redmine_api = Blueprint('redmine_api', __name__, url_prefix = '/redmine')


@job_api.route('/', methods=['GET'])
def getJobs():
    """
    Endpoint returning a list of jobs
    ---
    tags:
      - Job
    responses:
      200:
        description: A list of job
    """
    all_jobs = scheduler.get_jobs()
    return Response(str(all_jobs))

@job_api.route('/', methods=['POST'])
def addJob():
    """
    Endpoint to create new Job
    ---
    tags:
      - Job
    parameters:
      - name: body
        in: body
        type: string
        required: true
        schema:
          id: job
          required:
            - redminename
              username
              password
              job_id
              time
          properties:
            redminename:
              type: string
              description: The redmine's name.
              default: "Lu jin"
            username:
              type: string
              description: The redmine's username.
              default: "User name"
            password:
              type: string
              description: The redmine's password.
              default: "password"
            job_id:
              type: string
              description: The job's id.
              default: "job1"
            time:
              type: string
              description: The job's time (s).
              default: "60"
            notes:
              type: string
              description: The job's notes.
              default: "您好，工单已经收到，正在处理中"
    responses:
      200:
        description: An object of job  which is created
    """
    try:
        username = request.json['username']
        password = request.json['password']
        name = request.json['redminename']
        notes = request.json['notes']
        args = (username, password, name, notes)
        job_id = request.json['job_id']
        time = request.json['time']
        auth = auth_redmine(username, password)
        if auth == "ok":
            scheduler.add_job(id=str(job_id), func=Reply_redmine, args=args, trigger='interval', seconds=int(time))
            msg = {
                "status": "success",
                "job_id": job_id,
                "action": "add job"
            }
            return Response(json.dumps(msg), content_type='application/json')
        else:
            msg = {
                "status": "failed",
                "job_id": job_id,
                "action": "add job",
                "error": auth
            }
            return Response(json.dumps(msg), content_type='application/json',status=401)
    except Exception as e:
        msg = {
            "status": "failed",
            "action": "add job",
            "error": str(e)
        }
        return Response(json.dumps(msg), content_type='application/json', status=400)

@job_api.route('/', methods=['DELETE'])
def deleteJob():
    """
    Endpoint to delete a job
    ---
    tags:
      - Job
    parameters:
      - name: job_id
        in: query
        type: string
        required: true
    responses:
      200:
        description: An object of user  which is created
    """
    job_id = request.args.get('job_id')
    try:
        scheduler.remove_job(job_id)
        msg = {
            "status": "success",
            "job_id": job_id
        }
        return Response(json.dumps(msg), content_type='application/json')
    except Exception as e:
        msg = {
            "status": "failed",
            "error": str(e)
        }
        return Response(json.dumps(msg), content_type='application/json')


@redmine_api.route('/', methods=['POST'])
def redmine():
    """
    Endpoint to run one time redmine
    ---
    tags:
      - Redmine
    parameters:
      - name: body
        in: body
        type: string
        required: true
        schema:
          id: Redmine
          required:
            - redminename
              username
              password
          properties:
            redminename:
              type: string
              description: The redmine's name.
              default: "Lu jin"
            username:
              type: string
              description: The redmine's username.
              default: "User name"
            password:
              type: string
              description: The redmine's password.
              default: "password"
            notes:
              type: string
              description: The job's notes.
              default: "您好，工单已经收到，正在处理中"
    responses:
      200:
        description: An object of job  which is created
    """
    try:
        username = request.json['username']
        password = request.json['password']
        notes = request.json['notes']
        name = request.json['redminename']
        status, issue_list = Reply_redmine(username, password, name, notes)
        issue_list_str = str(issue_list)

        if status == "success":
            msg = {
                "status": status,
                "job_id": issue_list_str,
            }
            return Response(json.dumps(msg), content_type='application/json')
        else:
            msg = {
                "status": status,
                "error": issue_list_str,
            }
            return Response(json.dumps(msg), content_type='application/json',status=401)
    except Exception as e:

        return Response(str(e))
