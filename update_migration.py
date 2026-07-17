import re

with open('d:/project_vps/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

migration_code = '''    try:
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE "user" ADD COLUMN wallet_balance FLOAT DEFAULT 0.0'))
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    try:
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE "user" ADD COLUMN full_name VARCHAR(100)'))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        
    try:
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE "user" ADD COLUMN email VARCHAR(120)'))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        
    try:
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE "user" ADD COLUMN phone VARCHAR(20)'))
        db.session.commit()
    except Exception as e:
        db.session.rollback()'''
        
content = re.sub(r'    try:\n        from sqlalchemy import text\n        db\.session\.execute\(text\(\'ALTER TABLE "user" ADD COLUMN wallet_balance FLOAT DEFAULT 0\.0\'\)\)\n        db\.session\.commit\(\)\n    except Exception as e:\n        db\.session\.rollback\(\)', migration_code, content)

with open('d:/project_vps/app.py', 'w', encoding='utf-8') as f:
    f.write(content)
