from redminelib import Redmine
from flask import Flask

app = Flask(__name__)
import logging
app.logger.setLevel(logging.INFO)


def auth_redmine(username, password):
    redmine = Redmine('http://ticket.wise-paas.com', username=username, password=password)
    try:
        redmine.auth()
        return "ok"
    except Exception as e:
        return "auth failed: " + str(e)

def Reply_redmine (username, password, name, notes):
    app.logger.info("start runing Reply_redmine by %s", username)
    redmine = Redmine('http://ticket.wise-paas.com', username=username, password=password)
    auth = auth_redmine(username, password)
    app.logger.info("auth is" + auth)
    if auth == "ok":
        routine_id = list(redmine.issue.all(limit=10).filter(project__id=36, assigned_to__name=name, status__name='New').values('id'))
        all_id = list(redmine.issue.all(limit=10).filter(assigned_to__name=name, status__name='New').values('id'))
        issue_list = []
        if all_id:
            for id in all_id:
                if id not in routine_id:
                    issues_id = id['id']
                    app.logger.info("issues_id: %s",issues_id)
                    issue = redmine.issue.get(issues_id)
                    issue.save(status_id=2, notes=notes)
                    issue_list.append(issue)
            app.logger.info("end runing Reply_redmine by %s", username)
        else:
            app.logger.warn("no issue or error for login api; username:" + username + "; password:" + password)
        return "success", issue_list

    else:
        return "failed", auth


    # except Exception as e:
    #     print(e)
    #     issue_list = [str(e)]
    #     app.logger.error(str(e))
    #     return "failed", issue_list


