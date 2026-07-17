import re

# 1. Update static/app.js
with open('d:/project_vps/static/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

app_js = app_js.replace("prefill: data.prefill,", "prefill: data.prefill,\n          customer_id: data.customer_id,\n          remember_customer: true,")

with open('d:/project_vps/static/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

# 2. Update wallet.html
with open('d:/project_vps/templates/wallet.html', 'r', encoding='utf-8') as f:
    wallet = f.read()

wallet = wallet.replace("prefill: data.prefill,", "prefill: data.prefill,\n                    customer_id: data.customer_id,\n                    remember_customer: true,")

with open('d:/project_vps/templates/wallet.html', 'w', encoding='utf-8') as f:
    f.write(wallet)

# 3. Update ip-checkout.html
with open('d:/project_vps/templates/ip-checkout.html', 'r', encoding='utf-8') as f:
    ip_chk = f.read()

ip_chk = ip_chk.replace("prefill: data.prefill,", "prefill: data.prefill,\n                    customer_id: data.customer_id,\n                    remember_customer: true,")

with open('d:/project_vps/templates/ip-checkout.html', 'w', encoding='utf-8') as f:
    f.write(ip_chk)

