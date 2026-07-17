import re

with open('d:/project_vps/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add company_name migration
migration = '''    try:
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE "user" ADD COLUMN company_name VARCHAR(100)'))
        db.session.commit()
    except Exception as e:
        db.session.rollback()'''
        
content = re.sub(r'(db\.session\.rollback\(\))', r'\1\n\n' + migration, content, count=1)

# Update /profile route to save company_name
content = content.replace("user.phone = request.form.get('phone')", "user.phone = request.form.get('phone')\n        user.company_name = request.form.get('company_name')")

with open('d:/project_vps/app.py', 'w', encoding='utf-8') as f:
    f.write(content)

