import MySQLdb
import datetime

# ---------- variable setup ----------

connected = False
database = None
cursor = None

def setUp():
	global database
	global cursor
	global connected

	if not connected:
		try:
			database = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="Revisions_CM")
			cursor = database.cursor()
			connected = True
		except Exception as e:
			print "no"
			connected = False

	print "DB connection established: {}".format(connected)

def end():
	global connected
	if connected:
		database.close()
		connected = False

	print "DB connection closed: {}".format(not connected)

def retrieveProjects():
	query = "SELECT * FROM projects"
	cursor.execute(query)
	return cursor.fetchall()

def retrieveReleases(project):
	query = "SELECT release_name FROM releases WHERE project_name = %s"
	#query = "SELECT branch_name FROM Branches"
	cursor.execute(query, (project,))
	return cursor.fetchall()

def retrieveBuilds(release, project):
	query = "SELECT build_name, build_path, build_state FROM builds WHERE release_name = %s AND project_name = %s"
	cursor.execute(query, (release, project))
	return cursor.fetchall()

def retrieveBuild(build):
	query = "SELECT build_name, build_path, build_state FROM builds WHERE build_name = %s"
	cursor.execute(query, (build,))
	builds = cursor.fetchall()
	print builds
	return builds

def retrievePRinfo(build_name):
	query = "SELECT pr_number FROM pr_info WHERE build_name = %s" 
	cursor.execute(query, (build_name,))
	return cursor.fetchall()

def retrieveRevision(build_name): 
	query = "SELECT commit_number FROM builds WHERE build_name = %s"
	cursor.execute(query, (build_name,))
	return cursor.fetchall()

def retrieveCM(cm_hash):
	query = "SELECT cm_blob from revision WHERE commit_number = %s"
	cursor.execute(query, (cm_hash,))
	return cursor.fetchall()


