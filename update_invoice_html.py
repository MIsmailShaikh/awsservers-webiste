import re

with open('d:/project_vps/templates/invoice.html', 'r', encoding='utf-8') as f:
    content = f.read()

company_field = '''                <strong>Billed To:</strong><br>
                {% if user.company_name %}{{ user.company_name }}<br>{% endif %}
                {{ user.full_name or user.username }}<br>'''
      
content = content.replace("                <strong>Billed To:</strong><br>\n                {{ user.full_name or user.username }}<br>", company_field)

with open('d:/project_vps/templates/invoice.html', 'w', encoding='utf-8') as f:
    f.write(content)
