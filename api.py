import os
import stripe
from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime, timedelta, timezone

def todayDate():
    today = datetime.today()
    tdate = today.strftime('%Y-%m-%d')
    return tdate

app = Flask(__name__)
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

PLANS = {
    "Monthly": {"price_id": "price_1UdWAh0mMuJIAd5uRNZYabo9", "mode": "subscription"},
    "One Time": {"price_id": "price_1UdWAh0mMuJIAd5uVXTumuD7", "mode": "payment"},
    "Yearly": {"price_id": "price_1UdWAh0mMuJIAd5u22zNY1oM", "mode": "subscription"},
}

def get_db():
    return psycopg2.connect(os.getenv("CC_CONNECTION"))

@app.route("/price-plan", methods=["POST"])
def price_plan():
    return jsonify({"One time": 20.00, "Monthly": 10.00, "Annually": 120.00})

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
            success_url="https://courier-control.onrender.com/success?session_id={CHECKOUT_SESSION_ID}&email={email}&name={name}&plan={plan}",
            cancel_url="https://courier-control.onrender.com/cancel",
        )

        return jsonify({"checkout_url": session.url, "session_id": session.id})

    except Exception as e:
        print("STRIPE ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/success")
def payment_success():
    session_id = request.args.get("session_id")
    email = request.args.get("email")
    name = request.args.get("name")
    plan = request.args.get("plan")
    tdate = todayDate()
    if session_id:
        session = stripe.checkout.Session.retrieve(session_id)
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""INSERT INTO customer_plan (company, name, address1, address2, city, postcode, job_title, email, username, password, NOW(), date, session, subscription_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",("", name, "", "", "", "", "", email, "", "", tdate, session_id, plan))

        conn.commit()
        cur.close()
        conn.close()
        if session.payment_status == "paid":
            return "Payment successful! You can close this browser tab and return to Courier Control."
    return "Payment pending or invalid.", 400

@app.route("/check-paid", methods=["POST"])
def checkIfPaid():

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No Data Received From User"}), 400

    username = data["username"]
    email = data["email"]
    session = data["session_id"]
    con = get_db()
    cur = con.cursor()

    cur.execute("""SELECT subscription_type, date, session FROM customer_plan WHERE email = %s OR username = %s OR session = %s ORDER BY id DESC LIMIT 1""",(email, username, session))

    row = cur.fetchone()

    con.commit()
    con.close()
    cur.close()

    if row:
        subscription = row[0]
        paid_date = row[1]
        session = row[2]

        if subscription == 'One Time':
            if isinstance(paid_date, datetime):
                paid_date = paid_date.date()
            elif isinstance(paid_date, str):
                paid_date = datetime.strptime(paid_date.strip(), "%Y-%m-%d").date()

            today_utc = datetime.now(timezone.utc).date()
            date_elapsed = (today_utc - paid_date).days

            if date_elapsed <= 31:
                return jsonify({"success": True})
            else:
                return jsonify({"error": False})
        else:
            try:
                active = is_subscription_active(session_id = session)
                if active:
                    return jsonify({"success": True, "active": True})
                return jsonify({"success": False, "active": False})
            except Exception as e:
                print("STRIPE CHECK ERROR", str(e))
                return jsonify({"error": str(e)}), 500


@app.route("/cancel")
def payment_cancel():
    return "Payment cancelled. You can close this browser tab and return to Courier Control."

if __name__ == "__main__":
    app.run(port=5000, debug=True)