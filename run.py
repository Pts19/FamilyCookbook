from flaskblog import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    #Always runs the flask server by running the module
    #instead of "export FLASK_APP=flaskblog.py"
    #app.run(debug=True) -> instead of export FLASK_DEBUG = 1
    #This is used in the documentation now, so maybe this is the best way
