from flask import Flask, request, redirect
import connexion

def create_app():
    app = connexion.App(__name__, port=8080, specification_dir='swagger/')
    app.add_api('helloworld.yml', arguments={'title': 'Hello World AMQ'})

    return app

flask_app = create_app()
