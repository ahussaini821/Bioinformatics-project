from flask import Flask, render_template
import mysql.connector


#create flask application
app = Flask(__name__)

#tell code where to find the database
mydatabase = mysql.connector.connect(host ="localhost",
									 user= "root",
									 passwd = "44Gt66pa", database = "data_test")
mycursor= mydatabase.cursor()
#protein_table_file = "protein_example.csv"

#define the action for main page
@app.route("/")
def index():
	return render_template("index_page.html")

@app.route("/example")
def example():
	mycursor.execute("SELECT * FROM tableofproteins")
	data = mycursor.fetchall()
	return render_template("example.html", output_data = data)
#start the web server
if __name__ == "__main__":
	app.run(debug=True)

