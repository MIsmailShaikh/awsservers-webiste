# -*- coding: utf-8 -*-
import os
import re

html_files = [
    'd:/project_vps/templates/index.html',
    'd:/project_vps/templates/pricing.html',
    'd:/project_vps/templates/wallet.html',
    'd:/project_vps/templates/manage.html',
    'd:/project_vps/templates/ip-checkout.html',
]

for fpath in html_files:
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove Cashfree script tag
        content = re.sub(r'<script src="https://sdk\.cashfree\.com/js/v3/cashfree\.js"></script>\n?', '', content)
        
        # Remove wallet cashfree text
        content = content.replace(" Payments are processed securely via Cashfree.", "")
        
        # In wallet.html, remove Cashfree checkout logic
        content = re.sub(r'const cashfree = Cashfree\(\{.*?\}\);', '', content, flags=re.DOTALL)
        content = re.sub(r'cashfree\.checkout\(\{.*?\}\);', 'alert("Payment system under maintenance. Please contact support.");', content, flags=re.DOTALL)
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

appjs_path = 'd:/project_vps/static/app.js'
with open(appjs_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Remove Cashfree mode
js_content = re.sub(r'const CASHFREE_MODE = "sandbox"; // "sandbox" \| "production"\n', '', js_content)
js_content = re.sub(r'// NovaVPS.*?Configure Cashfree below.', '// AVPSSERVER \u2014 plain JS.', js_content)

# Remove FAQ cashfree text
js_content = js_content.replace('Checkout is powered by Cashfree \u2014 ', '')

# Gut the createCheckoutSession function
new_checkout_func = '''async function createCheckoutSession(planId) {
    alert("Our payment system is currently being upgraded. Please contact support to complete your purchase.");
    // Simulate throwing an error to stop the UI spinner
    throw new Error("Payment system maintenance");
}'''
js_content = re.sub(r'async function createCheckoutSession\(planId\) \{[\s\S]*?(?=\nasync function generateIPCheckoutSession)', new_checkout_func + '\n', js_content)

new_ip_checkout_func = '''async function generateIPCheckoutSession(ipId) {
    alert("Our payment system is currently being upgraded. Please contact support to complete your purchase.");
    throw new Error("Payment system maintenance");
}'''
js_content = re.sub(r'async function generateIPCheckoutSession\(ipId\) \{[\s\S]*?(?=$)', new_ip_checkout_func + '\n', js_content)

with open(appjs_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

