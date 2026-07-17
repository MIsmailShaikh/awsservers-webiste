import os
import re

# Update HTML files with Razorpay Key
html_files = [
    'd:/project_vps/templates/index.html',
    'd:/project_vps/templates/pricing.html',
    'd:/project_vps/templates/wallet.html',
    'd:/project_vps/templates/manage.html',
    'd:/project_vps/templates/ip-checkout.html',
]

key_script = '  <script>window.RAZORPAY_KEY = "{{ razorpay_key_id }}";</script>\n'

for fpath in html_files:
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'window.RAZORPAY_KEY' not in content:
            content = content.replace('  <script src="https://checkout.razorpay.com/v1/checkout.js"></script>', key_script + '  <script src="https://checkout.razorpay.com/v1/checkout.js"></script>')
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)

# Update static/app.js
with open('d:/project_vps/static/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

new_checkout_js = '''// ------------------ Razorpay checkout ------------------
document.querySelectorAll("button.buy").forEach(btn => {
  btn.addEventListener("click", async () => {
    const plan = PLANS.find(p => p.id === btn.dataset.plan);
    try {
      btn.disabled = true;
      const original = btn.innerHTML;
      btn.innerHTML = "Opening checkout…";
      
      const response = await fetch('/create-order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plan_id: plan.id })
      });
      const data = await response.json();
      
      if (response.ok && data.order_id) {
        const options = {
          key: window.RAZORPAY_KEY,
          amount: data.amount,
          currency: data.currency,
          name: "AVPSSERVER",
          description: "VPS Purchase - " + plan.name,
          order_id: data.order_id,
          handler: async function (response) {
            // Verify payment
            const verifyRes = await fetch('/verify-payment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    razorpay_payment_id: response.razorpay_payment_id,
                    razorpay_order_id: response.razorpay_order_id,
                    razorpay_signature: response.razorpay_signature,
                    context: 'vps'
                })
            });
            const verifyData = await verifyRes.json();
            if (verifyRes.ok && verifyData.status === 'success') {
                window.location.href = '/simulate-vps-success';
            } else {
                alert("Payment verification failed!");
            }
          },
          theme: { color: "#673de7" }
        };
        const rzp = new window.Razorpay(options);
        rzp.on('payment.failed', function (response){
            alert("Payment failed: " + response.error.description);
        });
        rzp.open();
      } else {
        alert("Failed to create order: " + (data.error || 'Unknown error'));
      }
      btn.innerHTML = original;
    } catch (e) {
      alert("Checkout error: " + (e.message || e));
      btn.innerHTML = "Buy " + plan.name + " &rarr;";
    } finally {
      btn.disabled = false;
    }
  });
});'''

app_js = re.sub(r'// ------------------ Cashfree checkout ------------------[\s\S]*?(?=\n// ------------------ Terminal Animation ------------------)', new_checkout_js, app_js)

with open('d:/project_vps/static/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

# Update templates/wallet.html
with open('d:/project_vps/templates/wallet.html', 'r', encoding='utf-8') as f:
    wallet = f.read()

wallet_js_new = '''
            if (response.ok && data.order_id) {
                // Step 2: Initialize Razorpay Checkout
                const options = {
                    key: window.RAZORPAY_KEY,
                    amount: data.amount,
                    currency: data.currency,
                    name: "AVPSSERVER",
                    description: "Wallet Topup",
                    order_id: data.order_id,
                    handler: async function (res) {
                        const verifyRes = await fetch('/verify-payment', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                razorpay_payment_id: res.razorpay_payment_id,
                                razorpay_order_id: res.razorpay_order_id,
                                razorpay_signature: res.razorpay_signature,
                                context: 'wallet'
                            })
                        });
                        const verifyData = await verifyRes.json();
                        if (verifyRes.ok && verifyData.status === 'success') {
                            window.location.href = '/simulate-wallet-success/' + data.order_id;
                        } else {
                            alert("Payment verification failed!");
                        }
                    },
                    theme: { color: "#673de7" }
                };
                const rzp = new window.Razorpay(options);
                rzp.on('payment.failed', function (res){
                    alert("Payment failed: " + res.error.description);
                });
                rzp.open();
                btn.innerHTML = originalText;
                btn.disabled = false;
            } else {'''

wallet = re.sub(r'if \(response\.ok && data\.payment_session_id\) \{[\s\S]*?\} else \{', wallet_js_new, wallet)

with open('d:/project_vps/templates/wallet.html', 'w', encoding='utf-8') as f:
    f.write(wallet)

# Update templates/ip-checkout.html
with open('d:/project_vps/templates/ip-checkout.html', 'r', encoding='utf-8') as f:
    ip_chk = f.read()
    
ip_js_new = '''
            if (response.ok && data.order_id) {
                // Step 2: Initialize Razorpay Checkout
                const options = {
                    key: window.RAZORPAY_KEY,
                    amount: data.amount,
                    currency: data.currency,
                    name: "AVPSSERVER",
                    description: "Static IP Checkout",
                    order_id: data.order_id,
                    handler: async function (res) {
                        const verifyRes = await fetch('/verify-payment', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                razorpay_payment_id: res.razorpay_payment_id,
                                razorpay_order_id: res.razorpay_order_id,
                                razorpay_signature: res.razorpay_signature,
                                context: 'ip'
                            })
                        });
                        const verifyData = await verifyRes.json();
                        if (verifyRes.ok && verifyData.status === 'success') {
                            window.location.href = '/simulate-ip-success/{{ ip_id }}';
                        } else {
                            alert("Payment verification failed!");
                        }
                    },
                    theme: { color: "#673de7" }
                };
                const rzp = new window.Razorpay(options);
                rzp.on('payment.failed', function (res){
                    alert("Payment failed: " + res.error.description);
                });
                rzp.open();
                btn.innerHTML = originalText;
                btn.disabled = false;
            } else {'''
            
ip_chk = re.sub(r'if \(response\.ok && data\.payment_session_id\) \{[\s\S]*?\} else \{', ip_js_new, ip_chk)

with open('d:/project_vps/templates/ip-checkout.html', 'w', encoding='utf-8') as f:
    f.write(ip_chk)

