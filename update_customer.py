import re

with open('d:/project_vps/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add migration
migration = '''    try:
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE "user" ADD COLUMN razorpay_customer_id VARCHAR(100)'))
        db.session.commit()
    except Exception as e:
        db.session.rollback()'''
        
content = re.sub(r'(db\.session\.rollback\(\))', r'\1\n\n' + migration, content, count=1)

# Update /profile route to create customer
profile_update = '''        user.company_name = request.form.get('company_name')
        
        if not user.razorpay_customer_id:
            try:
                cust = razorpay_client.customer.create({
                    "name": user.full_name,
                    "email": user.email,
                    "contact": user.phone
                })
                user.razorpay_customer_id = cust['id']
            except Exception as e:
                print(f"Failed to create Razorpay customer: {e}")
                
        db.session.commit()'''
        
content = content.replace("user.company_name = request.form.get('company_name')", profile_update)

# Update return JSON in create_order endpoints
prefill_update = '''            "prefill": {
                "name": user.full_name,
                "email": user.email,
                "contact": user.phone
            },
            "customer_id": user.razorpay_customer_id'''
content = content.replace('''            "prefill": {
                "name": user.full_name,
                "email": user.email,
                "contact": user.phone
            }''', prefill_update)

with open('d:/project_vps/app.py', 'w', encoding='utf-8') as f:
    f.write(content)
