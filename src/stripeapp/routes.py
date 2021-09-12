import os
import stripe
from flask import jsonify, render_template, url_for, redirect, request, abort
from stripeapp import app, db
from stripeapp.forms import LoginForm, RegisterForm
from stripeapp.models import User, StripeCustomer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

stripe_keys = {
    "secret_key": app.config['STRIPE_SECRET_KEY'],
    "publishable_key": app.config['STRIPE_PUBLISHABLE_KEY'],
    "price_id": app.config['STRIPE_PRICE_ID']
}

stripe.api_key = stripe_keys["secret_key"]


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    stripe_customer_data = StripeCustomer.query.filter_by(user_id=current_user.id).first()
    if stripe_customer_data:
        stripe_subscribed = True
    else:
        stripe_subscribed = False
    return render_template('index.html', email=current_user.email, is_stripe_subscribed=stripe_subscribed)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user:
            if check_password_hash(user.password, login_form.password.data):
                login_user(user, remember=login_form.remember.data)
                return redirect(url_for('index'))
        return '<h1> Invalid Username or Password </h1>'
    return render_template('login.html', form=login_form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        hashed_password = generate_password_hash(register_form.password.data, method='sha256')
        new_user = User(email=register_form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1> New user created </h1>'

    return render_template('signup.html', form=register_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/stripe_subscription')
def stripe_subscription():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            customer_email= current_user.email,
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

@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG and Invalid')
        abort(400)

    payload = request.data
    endpoint_secret = app.config['STRIPE_ENDPOINT_SECRET']
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return jsonify({'error': str(e)})
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify({'error': str(e)})

    if event["type"] == "checkout.session.completed":
        session = event.data.object
        handle_checkout_session(session)

    return jsonify({'status': 'success'})


def handle_checkout_session(session):
    user = User.query.filter_by(email=session['customer_details']['email']).first()
    if user:
        new_subscription = StripeCustomer(user_id=user.id, stripe_customer_id=session['customer'], stripe_subscription_id=session['subscription'] )
        db.session.add(new_subscription)
        db.session.commit()
        print("Subscription was successful.")
    else:
        print("please provide valid email")