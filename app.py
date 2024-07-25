from flask import Flask, render_template, request, session, redirect, url_for, make_response
import db

app = Flask(__name__)
app.secret_key = 'blablakey'

app.config.update(
    SESSION_COOKIE_HTTPONLY=False,
    SESSION_COOKIE_SAMESITE='Lax'  
)

block_list = ["<script>", "</sciprt>", "alert", 'cookie']

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        session['user_id'] = gen_userId()
        
    if request.method == 'POST':
        db.add_comment(request.form['comment'])
        return redirect(url_for('index'))
        
    search_query = request.args.get('q')
    for item in block_list:
        if search_query == None or item not in search_query:
            comments = db.get_comments(search_query)
        else:  
            comments = ''
            search_query = 'not allowed character'
        
    # r = make_response(render_template('index.html',
    #                   comments=comments,
    #                   search_query=search_query))
    # r.headers.set('Content-Security-Policy', "script-src 'none'")
    # uncomment to enable CSP
    return render_template('index.html',
                      comments=comments,
                      search_query=search_query)

def gen_userId():
    import uuid
    return str(uuid.uuid4())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)