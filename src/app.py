import os
import stripe
from flask import Flask, jsonify, render_template, request, url_for

# Init app
app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
    "price_id": "price_1JNHzxLWZKsH5JrEna6EiqWY"
}

stripe.api_key = stripe_keys["secret_key"]

domain_url = 'http://localhost:5000'


@app.route('/')
def index():
    return render_template(
        'index.html'
    )

@app.route('/stripe_subscription')
def stripe_subscription():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": stripe_keys["price_id"],
                    "quantity": 1,
                }
            ],
            success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('index', _external=True)
        )
        return jsonify({"checkout_session_id": checkout_session['id'],"checkout_public_key": stripe_keys['publishable_key'] })
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == "__main__":
    app.run(debug=True)