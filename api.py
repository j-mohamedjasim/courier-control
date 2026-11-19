import os
import stripe
from flask import Flask, request, jsonify

app = Flask(__name__)
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

PLANS = {
    "Monthly": {"price_id": "price_1UdWAh0mMuJIAd5uRNZYabo9", "mode": "subscription"},
    "One Time": {"price_id": "price_1UdWAh0mMuJIAd5uVXTumuD7", "mode": "payment"},
    "Yearly": {"price_id": "price_1UdWAh0mMuJIAd5u22zNY1oM", "mode": "subscription"},
}


@app.route("/create-checkout", methods=["POST"])
def create_checkout():
    data = request.get_json()
    if not data or data.get("selected_plan") not in PLANS:
        return jsonify({"error": "Invalid plan selected"}), 400

    plan = PLANS[data["selected_plan"]]

    try:
        customer = stripe.Customer.create(
            name=data["name"],
            email=data["email"],
            address={"postal_code": data["postcode"], "country": "GB"},
        )

        session = stripe.checkout.Session.create(
            mode=plan["mode"],
            customer=customer.id,
            line_items=[{"price": plan["price_id"], "quantity": 1}],
            success_url="https://example.com/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://example.com/cancel",
        )

        return jsonify({"checkout_url": session.url, "session_id": session.id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/success")
def payment_success():
    session_id = request.args.get("session_id")
    if session_id:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == "paid":
            return "Payment successful! You can close this browser tab and return to Courier Control."
    return "Payment pending or invalid.", 400


@app.route("/cancel")
def payment_cancel():
    return "Payment cancelled. You can close this browser tab and return to Courier Control."

if __name__ == "__main__":
    app.run(port=5000, debug=True)