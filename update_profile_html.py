import re

with open('d:/project_vps/templates/profile.html', 'r', encoding='utf-8') as f:
    content = f.read()

company_field = '''      <div>
        <label for="company_name" class="block text-sm font-semibold text-slate-700 mb-1">Company Name (Optional)</label>
        <input type="text" id="company_name" name="company_name" value="{{ user.company_name or '' }}"
               class="block w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-900 placeholder-slate-400 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary shadow-sm transition-colors"
               placeholder="Acme Corp">
      </div>
      
      <div class="pt-2">'''
      
content = content.replace('<div class="pt-2">', company_field)

with open('d:/project_vps/templates/profile.html', 'w', encoding='utf-8') as f:
    f.write(content)
