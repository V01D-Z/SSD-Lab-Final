import logging
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

app = Flask(__name__)

######################
# 1. Rate Limiting   #
######################
# ------------------------------------------------------------------------------
# We’ll use Flask-Limiter to apply rate limits on sensitive endpoints.
# By default, we limit all endpoints to 5 requests per minute (for demonstration).
# You could also apply route-specific decorators like @limiter.limit("5/minute").

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"]  # e.g., 5 requests per minute
)

######################
# 2. Content Security Policy (CSP)
######################
# ------------------------------------------------------------------------------
# Flask-Talisman can help add a CSP header among other security headers. 
# Below, we specify a sample CSP that restricts scripts to our own domain (self).
# You can tailor it to your needs (allow certain CDNs, etc.).

csp = {
    'default-src': [
        "'self'"
    ],
    'script-src': [
        "'self'"
        # You could add "'unsafe-inline'" if absolutely necessary
        # but that would weaken your security posture.
    ],
    'style-src': [
        "'self'"
    ]
}

# Initialize Talisman with our CSP settings.
# Talisman also sets other security headers (HSTS, X-Frame-Options, etc.) by default.
Talisman(app, content_security_policy=csp)

######################
# 3. Secure Headers
######################
# ------------------------------------------------------------------------------
# By using Flask-Talisman, we already have many secure headers set:
#  - Strict-Transport-Security (HSTS)
#  - X-Content-Type-Options
#  - X-XSS-Protection
#  - X-Frame-Options
# You can further customize them if needed.
#
# For instance, to force HTTPS in production and set a long HSTS max-age:
#
# Talisman(app,
#          content_security_policy=csp,
#          force_https=True,
#          strict_transport_security=True,
#          strict_transport_security_max_age=31536000,  # 1 year
#          frame_options='DENY'
# )

######################
# 4. Logging & Monitoring
######################
# ------------------------------------------------------------------------------
# We use Python's built-in logging to track important events such as failed login
# attempts. You can configure a dedicated log file, or use other logging handlers.

# Configure logging
logging.basicConfig(
    filename='app.log',          # logs will be stored in app.log
    level=logging.INFO,          # set the minimum logging level
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

@app.route('/')
def index():
    # Simple home route
    return "Welcome to the Secure Flask App!"

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5/minute")  # Apply specific rate limit for login route
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # Dummy check for user credentials (Replace with actual auth logic)
        if username == "admin" and password == "secret":
            app.logger.info("Successful login for user: %s", username)
            return jsonify({"message": "Login successful"}), 200
        else:
            # Log failed login attempts
            app.logger.warning("Failed login attempt for user: %s", username)
            return jsonify({"error": "Invalid credentials"}), 401
    return '''
    <form method="POST" action="/login">
        <p><input type="text" name="username" placeholder="Username"></p>
        <p><input type="password" name="password" placeholder="Password"></p>
        <p><input type="submit" value="Login"></p>
    </form>
    '''

@app.errorhandler(429)
def ratelimit_handler(e):
    # Handle rate limit errors
    return jsonify({"error": "Too many requests, please try again later."}), 429

if __name__ == '__main__':
    app.run(debug=True)
