from fileapi.app.flask import create_app

app = create_app({'migrate': True})
