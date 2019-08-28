import status as status
from flask import Flask,request
from flask_api import status
from redmine.main import Reply_redmine
import logging


# from apscheduler.schedulers.blocking import BlockingScheduler
# scheduler = BlockingScheduler()
# scheduler.add_job(func=Reply_redmine, args=("lu.jin@adasd","asdasd","asdasd"), max_instances=10, trigger='interval', seconds=3)
# scheduler._logger = logging

from flask_apscheduler import APScheduler


class Config(object):
    # JOBS = [
    #     {
    #         'id': 'job1',
    #         'func': 'redmine.main:Reply_redmine',
    #         'args': ("lu.jin@adasd","asdasd","asdasd"),
    #         'trigger': 'interval',
    #         'seconds': 10
    #     }
    # ]

    SCHEDULER_API_ENABLED = True
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 10}
    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 3
    }

app = Flask(__name__)

app.logger.setLevel(logging.INFO)
app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)


@app.route('/jobs', methods=['POST', 'GET', 'DELETE'])
def jobs():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = username.split('@')[1].replace(".","")
        args = (username, password, name)

        job_id = request.form['job_id']
        seconds = request.form['seconds']
        scheduler.add_job(id=job_id, func=Reply_redmine, args=args, trigger='interval', seconds=int(seconds))

        return "add:"+ job_id,status.HTTP_201_CREATED

    if request.method == 'DELETE':
        job_id = request.args.get('job_id')
        try:
            scheduler.remove_job(job_id)
            return "deleted:" + job_id, status.HTTP_201_CREATED
        except Exception as e:
            return str(e), status.HTTP_404_NOT_FOUND



    else:
        all_jobs = scheduler.get_jobs()
        return str(all_jobs), status.HTTP_200_OK



@app.route('/redmine', methods=['POST', 'GET'])

def redmine():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = username.split('@')[1].replace(".","")
        try:
            issue_list = Reply_redmine(username, password, name)
            app.logger.info(issue_list)
            if issue_list:
                text = " ".join(issue_list)
                return text,status.HTTP_201_CREATED
            else:
                app.logger.info("no issue")
                return "no issue",status.HTTP_201_CREATED
        except:
            app.logger.info("error for redmine")
            return status.HTTP_401_UNAUTHORIZED
    else:
        return "ok", status.HTTP_200_OK

if __name__ == '__main__':
    scheduler.start()
    app.run(host='0.0.0.0')

