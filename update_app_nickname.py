import re

with open('d:/project_vps/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update imports
content = content.replace("from models import db, User, VPSInstance, Transaction", "from models import db, User, VPSInstance, Transaction, StaticIPNickname")

# 2. Add route for update-ip-nickname
route_code = '''
@app.route('/update-ip-nickname', methods=['POST'])
def update_ip_nickname():
    if not session.get('logged_in'):
        return {"error": "Unauthorized"}, 401
        
    req_data = request.json
    ip_id = req_data.get('ip_id')
    nickname = req_data.get('nickname')
    
    if not ip_id:
        return {"error": "ip_id is required"}, 400
        
    user_id = session.get('user_id')
    nick_obj = StaticIPNickname.query.filter_by(user_id=user_id, ip_id=ip_id).first()
    
    if nickname:
        if nick_obj:
            nick_obj.nickname = nickname
        else:
            nick_obj = StaticIPNickname(user_id=user_id, ip_id=ip_id, nickname=nickname)
            db.session.add(nick_obj)
    else:
        # If empty nickname is sent, we can delete the record or set it to empty
        if nick_obj:
            db.session.delete(nick_obj)
            
    db.session.commit()
    return {"status": "success"}
'''
content = content.replace("@app.route('/transactions')", route_code + "\n@app.route('/transactions')")

# 3. Update static-ips route to attach nicknames
static_ips_route = '''@app.route('/static-ips')
def static_ips():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    user_id = session.get('user_id')
    payment_result = session.pop('payment_result', None)
    
    ips = get_static_ips()
    
    # Fetch user's nicknames
    nicknames = StaticIPNickname.query.filter_by(user_id=user_id).all()
    nickname_map = {n.ip_id: n.nickname for n in nicknames}
    
    for ip in ips:
        if ip['id'] in nickname_map:
            ip['nickname'] = nickname_map[ip['id']]
            
    return render_template('static-ips.html', ips=ips, payment_result=payment_result)'''

# We need to replace the existing static_ips route
import re
content = re.sub(r"@app\.route\('/static-ips'\).*?return render_template\('static-ips\.html', ips=ips, payment_result=payment_result\)", static_ips_route, content, flags=re.DOTALL)


with open('d:/project_vps/app.py', 'w', encoding='utf-8') as f:
    f.write(content)
