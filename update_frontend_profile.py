import re

# 1. Update static/app.js
with open('d:/project_vps/static/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

def replace_checkout(match):
    code = match.group(0)
    # Check profile error
    new_error_check = '''      if (response.ok && data.order_id) {
        const options = {
          key: window.RAZORPAY_KEY,
          amount: data.amount,
          currency: data.currency,
          name: "AVPSSERVER",
          description: "VPS Purchase - " + plan.name,
          order_id: data.order_id,
          prefill: data.prefill,
          handler: async function (response) {'''
    code = re.sub(r'      if \(response\.ok && data\.order_id\) \{[\s\S]*?handler: async function \(response\) \{', new_error_check, code)
    
    else_block = '''      } else if (data.error === "profile_incomplete") {
        window.location.href = '/profile';
      } else {
        alert("Failed to create order: " + (data.error || 'Unknown error'));
      }'''
    code = re.sub(r'      \} else \{\n        alert\("Failed to create order: " \+ \(data\.error \|\| \'Unknown error\'\)\);\n      \}', else_block, code)
    return code

app_js = re.sub(r'// ------------------ Razorpay checkout ------------------[\s\S]*?(?=\n// ------------------ Terminal Animation ------------------)', replace_checkout, app_js)

with open('d:/project_vps/static/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)


# 2. Update wallet.html
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
                    prefill: data.prefill,
                    handler: async function (res) {'''
wallet = re.sub(r'            if \(response\.ok && data\.order_id\) \{[\s\S]*?handler: async function \(res\) \{', wallet_js_new, wallet)

wallet_else = '''                btn.disabled = false;
            } else if (data.error === "profile_incomplete") {
                window.location.href = '/profile';
            } else {'''
wallet = re.sub(r'                btn\.disabled = false;\n            \} else \{', wallet_else, wallet)

with open('d:/project_vps/templates/wallet.html', 'w', encoding='utf-8') as f:
    f.write(wallet)


# 3. Update ip-checkout.html
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
                    prefill: data.prefill,
                    handler: async function (res) {'''
ip_chk = re.sub(r'            if \(response\.ok && data\.order_id\) \{[\s\S]*?handler: async function \(res\) \{', ip_js_new, ip_chk)

ip_else = '''                btn.disabled = false;
            } else if (data.error === "profile_incomplete") {
                window.location.href = '/profile';
            } else {'''
ip_chk = re.sub(r'                btn\.disabled = false;\n            \} else \{', ip_else, ip_chk)

with open('d:/project_vps/templates/ip-checkout.html', 'w', encoding='utf-8') as f:
    f.write(ip_chk)

