from flask import Flask, render_template, redirect, url_for, request, flash
from flask_pymongo import PyMongo
from gridfs import GridFS
# from werkzeug import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = '59d3ca27e6701d3fd06eb960ca5866a5'
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"

mongo = PyMongo(app)
FS = GridFS(mongo.db)

@app.route("/addQues", methods = ["POST", "GET"])
def addQues():
	data = request.form
	if(data):
		questions = mongo.db.questions
		input_files = request.files.getlist('in')
		output_files = request.files.getlist('out')

		# contains reference to file in id
		input_file_id = []
		output_file_id = []

		for inputFile,outputFile in zip(input_files, output_files):
			input_file_id.append( FS.put(inputFile) )
			output_file_id.append( FS.put(outputFile) )

		questions.insert({
			"prob_name" : data['name'],
			"prob_stmt" : data['statement'],
			"difficulty" : data['difficulty'],
			"testcase" : {
				"input" : input_file_id,
				"output" : output_file_id
			},
			"tag" : data['tags']
			})
		print("---------Input-----------")
		for i in range(len(input_file_id)):
			print(FS.get(input_file_id[i]).read())
		print("---------End-------------")

		print("---------Output-----------")
		for i in range(len(input_file_id)):
			print(FS.get(output_file_id[i]).read())
		print("---------End-------------")
	return render_template('admin.html')

@app.route("/test",methods = ["POST", "GET"])
def test():
	formData = request.form
	print("Files ->" , request.files)
	print("\n")
	print(len(request.files))
	return render_template("test.html")
if(__name__ == "__main__"):
	app.run(debug=True)