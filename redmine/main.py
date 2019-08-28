from redminelib import Redmine
from flask import Flask

app = Flask(__name__)
import logging
app.logger.setLevel(logging.INFO)

def Reply_redmine (username, password, name):
    app.logger.info("start runing Reply_redmine by %s", username)
    try:
        redmine = Redmine('http://ticket.wise-paas.com', username=username, password=password)
        routine_id = list(redmine.issue.all(limit=100).filter(project__id=36, assigned_to__name=name, status__name='New').values('id'))

        all_id = list(redmine.issue.all(limit=100).filter(assigned_to__name=name, status__name='New').values('id'))
        issue_list = []
        if all_id:
            for id in all_id:
                if id not in routine_id:
                    issues_id = id['id']
                    app.logger.info("issues_id: %s",issues_id)
                    issue = redmine.issue.get(issues_id)
                    issue.save(status_id=2, notes="您好，工单已经收到，正在处理中，谢谢")
                    issue_list.append(issue)
            app.logger.info("end runing Reply_redmine by %s", username)
        else:
            app.logger.warn("no issue or error for login redmine; username:" + username + "; password:" + password)
        return issue_list

    except:
        msg = "error for login redmine,username:" + username + "password:" + password
        issue_list = [msg]
        app.logger.error(msg)
        return issue_list


