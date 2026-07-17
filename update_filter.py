import re

with open('d:/project_vps/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

filter_code = '''
from datetime import timedelta

@app.template_filter('to_ist')
def to_ist_filter(dt):
    if not dt: return ""
    return dt + timedelta(hours=5, minutes=30)
'''

# Add the filter code before the first route definition
content = content.replace("@app.route('/', methods=['GET', 'POST'])", filter_code + "\n@app.route('/', methods=['GET', 'POST'])")

with open('d:/project_vps/app.py', 'w', encoding='utf-8') as f:
    f.write(content)
