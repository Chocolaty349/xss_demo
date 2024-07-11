from flask import Flask, render_template, request, session
import db

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Ensure this is a secure, random key

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        session['user_id'] = generate_user_id()

    if request.method == 'POST':
        db.add_comment(request.form['comment'])

    search_query = request.args.get('q')
    comments = db.get_comments(search_query)

    response = render_template('index.html', comments=comments, search_query=search_query)
    
    # Setting a session cookie securely
    session_cookie = session['user_id']
    response.set_cookie('session', session_cookie, httponly=False, secure=True, samesite='Lax')

    return response

def generate_user_id():
    import uuid
    return str(uuid.uuid4())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
