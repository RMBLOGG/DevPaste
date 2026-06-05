import sys
import os

# Add parent directory to path so app module can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

app = create_app()

# Vercel expects the app object to be named 'app'
if __name__ == '__main__':
    app.run(debug=False)
