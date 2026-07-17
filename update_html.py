import os

html_files = [
    'd:/project_vps/templates/index.html',
    'd:/project_vps/templates/pricing.html',
    'd:/project_vps/templates/wallet.html',
    'd:/project_vps/templates/manage.html',
    'd:/project_vps/templates/ip-checkout.html',
]

script_tag = '  <script src="https://checkout.razorpay.com/v1/checkout.js"></script>\n'

for fpath in html_files:
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'checkout.razorpay.com' not in content:
            # insert before </head>
            content = content.replace('</head>', script_tag + '</head>')
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)

