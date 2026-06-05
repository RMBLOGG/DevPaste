from flask import Flask
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

supabase: Client = None

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.secret_key = os.environ.get('SECRET_KEY', 'devpaste-secret-key-change-in-prod')

    global supabase
    supabase_url = os.environ.get('SUPABASE_URL', 'https://npiuthhiudgpjmwporyv.supabase.co')
    supabase_key = os.environ.get('SUPABASE_KEY', 'sb_publishable_MS-mBgtkEbkrVYpUuPzmbA_fYE17Xm2')
    supabase = create_client(supabase_url, supabase_key)

    from app.routes import main
    app.register_blueprint(main)

    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        return render_template('404.html'), 404

    return app

