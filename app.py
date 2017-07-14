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

@app.route('/get_help')
def get_help(): 
	return flask.render_template('/prdetails.html')

@app.route('/', methods=["GET", "POST"])
def testpage():
	if flask.request.method == "GET":
    		return flask.render_template('/testpage.html', projects = db.retrieveProjects(), builds = "")
	elif flask.request.method == "POST":
			try:
				 project = request.form['projects'].replace('+', ' ')
				 release = request.form['releases'].replace('+', ' ')
				 builds = db.retrieveBuilds(release, project)
				 print builds
				 return flask.render_template('testpage.html', projects=db.retrieveProjects(), newBuilds = builds)
			except: 
				return flask.render_template('testpage.html', projects=db.retrieveProjects())
@app.route('/prInfo')
def routePR():
		build = request.args.get('detailsButton')
		print build
		prInfo = db.retrievePRinfo(build)
		data = [{"pr_number": x[0], "responsible": gnats_pr.GnatsPr(int(x[0])).owner(), "pr_state": gnats_pr.GnatsPr(int(x[0])).state(), "synopsis": gnats_pr.GnatsPr(x[0]).run_query(r'''/usr/local/bin/query-pr --format '"%s" synopsis' ''' + str(x[0]))} for x in prInfo]
		return jsonify(data)

@app.route('/buildInfo')
def cmBuild():
	check = request.args.get('oneBuild')
	revision = db.retrieveRevision(check)
	print revision
	manifest = load_component_manifest_from_history(revision[0][0])
	repos = sorted(set(manifest.get_repos()))
	data = []
	for repo in repos:
		repo_instance = manifest.get_repo(repo)
		attributes = str(repo_instance.attributes)
		repo_revision = manifest.get_repo_revision(repo_instance)
		repo_components = repo_instance.get_components_list()
		comp = []
		for component in repo_components:
			compObj = manifest.get_component(component)
			comp.append({'component_name': component, 'component_revision': manifest.get_component_revision(compObj)})
			print comp
		data.append({'repo_name': repo, 'repo_revision': repo_revision, 'repo_components': comp, 'repo_attributes': attributes})

	return json.dumps({"data": data})	

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
			attributes = str(repo_instance.attributes)
			print "ATTRIBUTES", attributes
			repo_revision = manifest.get_repo_revision(repo_instance)
			repo_components = repo_instance.get_components_list()
			comp = []
			for component in repo_components:
				compObj = manifest.get_component(component)
				comp.append({'component_name': component, 'component_revision': manifest.get_component_revision(compObj)})
			data1.append({'repo_name': repo, 'repo_revision': repo_revision, 'repo_components': comp, 'repo_attributes': attributes})
			print data1
		print "len", len(removedRepos)
		for repo in removedRepos: 
			repo_instance = oldermanifest.get_repo(repo)
			attributes = str(repo_instance.attributes)
			repo_revision = oldermanifest.get_repo_revision(repo_instance)
			repo_components = repo_instance.get_components_list()
			comp = []
			for component in repo_components:
				compObj = oldermanifest.get_component(component)
				comp.append({'component_name': component, 'component_revision': oldermanifest.get_component_revision(compObj)})
				print comp
			data2.append({'repo_name': repo, 'repo_revision': repo_revision, 'repo_components': comp, 'repo_attributes': attributes})
		for repo in unchangedRepos: 
			repo_instance = manifest.get_repo(repo)
			attributes = str(repo_instance.attributes)
			print "ATTRIBUTES", attributes
			repo_instance2 = oldermanifest.get_repo(repo)
			repo_components = repo_instance.get_components_list()
			repo_components2 = repo_instance2.get_components_list()
			repo_revision = manifest.get_repo_revision(repo_instance)
			repo_revision2 = oldermanifest.get_repo_revision(repo_instance2)
			addedComponents = sorted(set(repo_components) - set(repo_components2))
			removedComponents = sorted(set(repo_components2) - set(repo_components))
			modifiedComponents = sorted(set(repo_components).intersection(set(repo_components2)))
			compAdded = []
			compRemoved = []
			compMod = []
			comp = []
			for component in addedComponents:
				compObj = manifest.get_component(component)
				compAdded.append({'component_name': component, 'component_revision': manifest.get_component_revision(compObj)})
			for component in removedComponents:
				compObj = oldermanifest.get_component(component)
				compRemoved.append({'component_name': component, 'component_revision': oldermanifest.get_component_revision(compObj)})
			for component in modifiedComponents: 
				compObj = oldermanifest.get_component(component)
				compObjNew = manifest.get_component(component)
				oldRevision = oldermanifest.get_component_revision(compObj)
				newRevision = manifest.get_component_revision(compObjNew)
				if (oldRevision != newRevision):
					compMod.append({'component_name': component, 'component_revision_old': oldRevision, 'component_revision_new': newRevision})
			comp.append(compAdded)
			comp.append(compRemoved)
			comp.append(compMod)
			if (repo_revision and repo_revision2) and (repo_revision != repo_revision2):
				data3.append({'repo_name': repo, 'repo_revision1': repo_revision2, 'repo_revision2': repo_revision, 'repo_components': comp, 'repo_attributes': attributes})
		data.append(data1)
		data.append(data2)
		data.append(data3)
		return json.dumps({"data": data})

def load_component_manifest_from_history (git_hash):  
	man = db.retrieveCM(git_hash)[0][0]
	with tempfile.NamedTemporaryFile(bufsize = 0) as tmpfile:
		tmpfile.write(man)
		return component_manifest.Manifest(tmpfile.name)
	

if __name__ == '__main__': 
	app.run()