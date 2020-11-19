from fileapi.app.flask import create_app
app = create_app({'migrate': True})

if __name__ == '__main__':
    app.run(debug=False)
