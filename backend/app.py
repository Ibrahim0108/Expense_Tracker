import os
from flask import Flask, send_from_directory,request
from routes.pin_routes import bp as pin_bp
from routes.user_routes import user_bp
from routes.monthly_routes import monthly_bp
from routes.expense_routes import expense_bp
from routes.deduction_routes import deduction_bp
from routes.lending_routes import lending_bp
from routes.Profile_routes import profile_bp
from routes.history_routes import history_bp
from routes.yearly_report import yearly_bp
from services.data_service import ensure_datafile
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")
    CORS(app)
    # secret key from env or default (change before publish)
    app.secret_key = os.environ.get("FLASK_SECRET", "change-me-please")
    # session timeout handled in lock_service; Flask session still used
    # Ensure data file exists on startup
    ensure_datafile()
    
    # Register blueprints
    app.register_blueprint(pin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(monthly_bp)
    app.register_blueprint(expense_bp) 
    app.register_blueprint(deduction_bp)
    app.register_blueprint(lending_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(yearly_bp)


    return app

app = create_app()

# Serve frontend dist (if using build)
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    dist = app.static_folder
    file_path = os.path.join(dist, path)
    # If the file exists in dist (e.g., JS, CSS, assets) → serve it
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        return send_from_directory(dist, path)
    return send_from_directory(dist, "index.html")

@app.errorhandler(404)
def handle_404(e):
    # Only redirect frontend routes, not API ones
    if not request.path.startswith("/api"):
        return send_from_directory(app.static_folder, "index.html")
    return e


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=debug)