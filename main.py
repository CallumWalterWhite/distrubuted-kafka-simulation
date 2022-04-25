from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    posts = [{
        'title': 'hello kit',
        'created': 'BLAHH'
    },{
        'title': 'super mario speed run',
        'created': 'UNDER 2mins!'
    }]
    return render_template('index.html', posts=posts)

app.run()