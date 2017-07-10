import os
import sys
from flask import render_template, json, request, Response, Flask, jsonify
from distutils.version import StrictVersion
import MySQLdb
import db
import flask
import re
import tempfile
sys.path.insert(1, os.environ["SANDBOX_TOOLS_LIB"])
import gnats_pr
import component_manifest
import git

app = Flask(__name__)
db.setUp()

@app.route('/getRelease')
def routeRelease(): 
	project = request.args.get('project')
	releases = db.retrieveReleases(project)
	data = [{"id": x[0], "name": x[0]} for x in releases]
	return jsonify(data)

@app.route('/details')
def details(): 
	return flask.render_template('/prdetails.html')

@app.route('/', methods=["GET", "POST"])
def testpage():
	if flask.request.method == "GET":
    		return flask.render_template('/testpage.html', projects = db.retrieveProjects(), builds = "")
	elif flask.request.method == "POST":
			try:
				 project = request.form['projects'].replace('+', ' ')
				 release = request.form['releases'].replace('+', ' ')
				 return flask.render_template('testpage.html', projects=db.retrieveProjects(), builds = db.retrieveBuilds(release, project))
			except: 
				return flask.render_template('testpage.html', projects=db.retrieveProjects())
@app.route('/prInfo')
def routePR():
		build = request.args.get('detailsButton')
		print build
		prInfo = db.retrievePRinfo(build)
		data = [{"pr_number": x[0], "responsible": gnats_pr.GnatsPr(int(x[0])).owner(), "pr_state": gnats_pr.GnatsPr(int(x[0])).state(), "synopsis": gnats_pr.GnatsPr(x[0]).run_query(r'''/usr/local/bin/query-pr --format '"%s" synopsis' ''' + str(x[0]))} for x in prInfo]
		return jsonify(data)

@app.route('/cmInfo')
def cmComparison():
		checked = request.args.get('twoBuilds')
		checked = checked.split();
		revision1 = db.retrieveRevision(checked[0]);
		revision2 = db.retrieveRevision(checked[1]);
		manifest1 = load_component_manifest_from_history(revision1[0][0])
		manifest2 = load_component_manifest_from_history(revision2[0][0])
		#manifest1 = component_manifest.load_component_manifest_from_history(revision1[0][0])
		#manifest2 = component_manifest.load_component_manifest_from_history(revision2[0][0])
		if (StrictVersion(manifest1.get_version()[-8:]) < StrictVersion(manifest2.get_version()[-8:])):
			addedRepos = sorted(set(manifest2.get_repos()) - set(manifest1.get_repos()))
			removedRepos = sorted(set(manifest1.get_repos()) - set(manifest2.get_repos()))
			unchangedRepos = sorted(set(manifest1.get_repos()).intersection(set(manifest2.get_repos())))
			manifest = manifest2
			oldermanifest = manifest1
		else: 
			addedRepos = sorted(set(manifest1.get_repos()) - set(manifest2.get_repos()))
			removedRepos = sorted(set(manifest2.get_repos()) - set(manifest1.get_repos()))
			unchangedRepos = sorted(set(manifest1.get_repos()).intersection(set(manifest2.get_repos())))
			manifest = manifest1
			oldermanifest = manifest2
		data1 = []
		data2 = []
		data = []
		data3 = []
		for repo in addedRepos: 
			repo_instance = manifest.get_repo(repo)
			repo_revision = manifest.get_repo_revision(repo_instance)
			data1.append({'repo_name': repo, 'repo_revision': repo_revision})
		for repo in removedRepos: 
			repo_instance = oldermanifest.get_repo(repo)
			repo_revision = oldermanifest.get_repo_revision(repo_instance)
			data2.append({'repo_name': repo, 'repo_revision': repo_revision})
		for repo in unchangedRepos: 
			repo_instance = manifest.get_repo(repo)
			repo_instance2 = oldermanifest.get_repo(repo)
			repo_revision = manifest.get_repo_revision(repo_instance)
			repo_revision2 = oldermanifest.get_repo_revision(repo_instance2)
			if (repo_revision and repo_revision2) and (repo_revision != repo_revision2):
				data3.append({'repo_name': repo, 'repo_revision1': repo_revision2, 'repo_revision2': repo_revision})

		data.append(data1)
		data.append(data2)
		data.append(data3)
		return json.dumps({"data": data})

def load_component_manifest_from_history (git_hash):    
	manifest = db.retrieveCM(git_hash)[0][0]
	with tempfile.NamedTemporaryFile(bufsize = 0) as tmpfile:
		tmpfile.write(manifest)
		return component_manifest.Manifest(tmpfile.name)


if __name__ == '__main__': 
	app.run()