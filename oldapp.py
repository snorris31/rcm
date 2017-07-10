from flask import render_template, json, request, Response, Flask, jsonify
import MySQLdb
import db
import flask


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
				 return flask.render_template('testpage.html', projects=db.retrieveProjects(), builds = db.retrieveBuilds(release))
			except: 
				return flask.render_template('testpage.html', projects=db.retrieveProjects())
@app.route('/prInfo')
def routePR():
		build = request.args.get('tempButton')
		print build
		prInfo = db.retrievePRinfo(build)
		data = [{"revision_number": x[0], "synopsis": x[1], "responsible": x[2]} for x in prInfo]
		print data
		return jsonify(data)


if __name__ == "__main__":
    app.run()
