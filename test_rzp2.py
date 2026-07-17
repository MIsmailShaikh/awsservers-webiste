import razorpay

key_id = "rzp_test_TEdx2Gbjmd267j"
key_secret = "xkfmwNucPANFVMxwsAmZTTqV"

client = razorpay.Client(auth=(key_id, key_secret))
try:
    order_data = {
        "amount": 1000,
        "currency": "INR",
        "receipt": "test_receipt_new"
    }
    order = client.order.create(data=order_data)
    print("Order created successfully:", order['id'])
except Exception as e:
    print("Exception details:", str(e))
