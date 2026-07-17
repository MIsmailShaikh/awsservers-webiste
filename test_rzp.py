import razorpay
import os

key_id = "rzp_test_TEct2G6clrhhry"
key_secret = "DMmXjR2jOk5CzBe8B1giJhJC"

client = razorpay.Client(auth=(key_id, key_secret))
try:
    order_data = {
        "amount": 1000,
        "currency": "INR",
        "receipt": "test_receipt_1"
    }
    order = client.order.create(data=order_data)
    print("Order created:", order)
except Exception as e:
    print("Exception details:", str(e))
    import traceback
    traceback.print_exc()
