from flaskblog import app
#from project folder flaskblog, import object "app"
#app used as application object to:
#make changes to database, use serialization,
#login manager, and encryption


if __name__ == "__main__":
    app.run(debug=True)
    #Always runs the flask server by running the module
    #instead of "export FLASK_APP=flaskblog.py"
    #app.run(debug=True) -> instead of export FLASK_DEBUG = 1
    #This is used in the documentation now, so maybe this is the best way
