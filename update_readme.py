import re

with open('d:/project_vps/README.txt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(' (Tailwind via CDN, Google Fonts, Cashfree SDK)', ' (Tailwind via CDN, Google Fonts)')
content = content.replace(' + Cashfree checkout wiring', '')
content = re.sub(r'Cashfree setup:.*', '', content, flags=re.DOTALL)

with open('d:/project_vps/README.txt', 'w', encoding='utf-8') as f:
    f.write(content)

with open('d:/project_vps/docker-compose.yml', 'r', encoding='utf-8') as f:
    dc = f.read()

dc = re.sub(r'\s+- CASHFREE_APP_ID=\$\{CASHFREE_APP_ID\}', '', dc)
dc = re.sub(r'\s+- CASHFREE_SECRET_KEY=\$\{CASHFREE_SECRET_KEY\}', '', dc)
dc = re.sub(r'\s+- CASHFREE_ENV=\$\{CASHFREE_ENV\}', '', dc)

with open('d:/project_vps/docker-compose.yml', 'w', encoding='utf-8') as f:
    f.write(dc)

