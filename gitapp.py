from flask import Blueprint,render_template, flash, redirect, session, url_for,send_from_directory, request, g, json,make_response
from flask import Flask
from flask.json import jsonify
from jinja2 import Markup, escape
from werkzeug import secure_filename
import json,requests,argparse,sys
from git import Repo
import os


application = Flask(__name__)

@application.route('/')
def index():
  return render_template('index.html')

@application.route('/clone_all',methods=['POST',"GET"])
def clone_all():
    data = json.loads(request.data.decode())
    target=data['username']
    from git import Repo
    url="https://api.github.com/users/" + target + "/repos"+'?client_id=f8d50aec9932f112aa96&client_secret=84cc2663717b5d68e87219b2e21c17a233c76545'
    r=requests.get(url)
    js_data=json.loads(r.content)
    for x in js_data:
        imgurl = x['owner']['avatar_url']
    filename = []
    for y in  js_data:
        cdict = {}
        cdict["reponame"] = y["name"]
        cdict['path'] = "https://github.com/"+target+'/'+y['name']
        cdict['download'] = "https://github.com/"+target+'/'+y['name']+'/archive/master.zip'
        filename.append(cdict)
    j = json.dumps(filename, indent=4)
    f = open('git.json', 'w')
    print >> f, j
    f.close()
    return jsonify(names=filename,img=imgurl)

@application.route('/clone_repos',methods=['POST','GET'])
def clone_repos():
    data = json.loads(request.data.decode())
    target=data['username']
    url="https://api.github.com/users/" + target + "/repos"+'?client_id=f8d50aec9932f112aa96&client_secret=84cc2663717b5d68e87219b2e21c17a233c76545'
    r=requests.get(url)
    js_data=json.loads(r.content)
    out = os.path.curdir
    output = out+'/cloned_repos/'
    print output
    for y in js_data:
        git_url=y["clone_url"]
        out_name=os.path.join(output, y["name"])
        if os.path.isdir(out_name):
            print git_url + ": Directory already existing - let me pull the fresh updates for you"
            repo=Repo(out_name);
            repo.remotes.origin.pull()
            return "done"
        else:
            Repo.clone_from(git_url, out_name)
            return "done"



if __name__ == '__main__':
    application.config.update(
            DEBUG=True,)
    application.run(host="0.0.0.0")
