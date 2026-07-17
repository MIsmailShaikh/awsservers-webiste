import re

# requirements.txt
with open('d:/project_vps/requirements.txt', 'r', encoding='utf-8') as f:
    reqs = f.read()
if 'razorpay' not in reqs:
    reqs += 'razorpay==1.4.1\n'
    with open('d:/project_vps/requirements.txt', 'w', encoding='utf-8') as f:
        f.write(reqs)

# .env
env_content = '''RAZORPAY_KEY_ID="rzp_test_TEct2G6clrhhry"
RAZORPAY_KEY_SECRET="DMmXjR2jOk5CzBe8B1giJhJC"
DATABASE_URL="sqlite:///awsservers.db"
'''
with open('d:/project_vps/.env', 'w', encoding='utf-8') as f:
    f.write(env_content)

# docker-compose.yml
with open('d:/project_vps/docker-compose.yml', 'r', encoding='utf-8') as f:
    dc = f.read()

if 'RAZORPAY_KEY_ID' not in dc:
    # insert after DATABASE_URL
    dc = dc.replace('      - DATABASE_URL=', '      - DATABASE_URL=\n      - RAZORPAY_KEY_ID=\n      - RAZORPAY_KEY_SECRET=')
    with open('d:/project_vps/docker-compose.yml', 'w', encoding='utf-8') as f:
        f.write(dc)

