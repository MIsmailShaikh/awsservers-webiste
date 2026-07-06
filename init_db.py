from app import app
from models import db, User, VPSInstance

with app.app_context():
    db.create_all()
    
    # Check if admin exists
    admin = User.query.filter_by(username='ismailzst643').first()
    if not admin:
        admin = User(username='ismailzst643')
        admin.set_password('1dsO#eK!y5')
        db.session.add(admin)
        db.session.commit()
        
        # Add a dummy VPS instance to match the UI
        vps = VPSInstance(
            user_id=admin.id,
            vps_id='56892AHF',
            name='edge-1',
            plan_name='Pro',
            status='Active',
            billing_date=16,
            due_date=20,
            monthly_price=33783.90
        )
        db.session.add(vps)
        db.session.commit()
        print("Database initialized with admin user and dummy VPS.")
    else:
        print("Admin user already exists.")
