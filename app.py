from tweetScraper import TwitterScrape
from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = "dfhvfukvwdvqkwebdvqygrfq3ufrvdviq3uvwjv3uvdvuqvb3vyq3hbbvqo3uw"
ts = TwitterScrape()
ts.login()
urls = []
@app.route('/')
def home():
    conn = get_db_connection()
    urls = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    tweets = session.get('tweets', None)
    if tweets:
        return render_template('index.html', urls = urls, tweets = tweets)
    else:
        return render_template('index.html', urls = urls)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    turl = request.form['url']
    conn = conn = get_db_connection()
    conn.execute('INSERT INTO posts (title, turl) VALUES (?, ?)',(title, turl))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/delete/<int:id>', methods=["POST"])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/fetch/<int:id>', methods=['POST'])
def fetch(id):
    conn = get_db_connection()
    turl = conn.execute('SELECT * FROM posts Where id = ?',(id,)).fetchall()
    conn.close()
    session['tweets'] = ts.get_tweets_from_list(turl[0]['turl'])
    return redirect(url_for('home'))



@app.route('/thread', methods=['POST'])
def thread():
    url = request.form['threadurl']
    if not url:
        flash("url is required")
    tweets = ts.get_tweets_from_list(url)
    i = 0
    tweets1 = []
    for tweet in tweets:
        if(i%2 != 0):
            i+=1
            continue
        tweets1.append( tweet)
        i+=1
        
        
    return render_template('index.html', tweets=tweets1)

if __name__ == '__main__':
    app.run(debug=True)

