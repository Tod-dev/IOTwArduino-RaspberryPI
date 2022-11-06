from flask import Flask

appname = 'http-server'
app = Flask(appname)

@app.route('/')
def home():
    return '<h1>Home</h1>'

if __name__ == '__main__':
    app.run()