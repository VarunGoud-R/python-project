from flask import Flask, abort, render_template, request

app = Flask(__name__)

# Custom 404 page
@app.errorhandler(404)
def not_found_error(error):
    print(error)
    return render_template('404.html'), 404

# Custom 500 page
@app.errorhandler(500)
def internal_server_error(error):
    print(error)
    return render_template('500.html'), 500

# Your routes go here
@app.route('/')
def home():
    print("Home Page")
    return render_template('index.html'), 200

# Example route that triggers a 404 error
@app.route('/400')
def not_found():
    # Raise an exception to trigger a 404 error
    # raise Exception("Page not found")
    # raise 404("Page not found!")
    abort(404)

# Example route that triggers a 500 error
@app.route('/500')
def internal_server_error_route():
    # Trigger a division by zero error to simulate a server error
    # result = 1 / 0
    # return str(result)
    # raise 500("Something went wrong!")
    abort(500)

def exception_handler(*args):
    if request.url.endswith('/'):
       return "PageError", 404
    else:
       return "Something went wrong!", 500
    
if __name__ == '__main__':
    app.run(debug=True)
