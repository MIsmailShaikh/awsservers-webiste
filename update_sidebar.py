import os
import glob

templates = glob.glob('d:/project_vps/templates/*.html')

profile_link = '''      <a href="/profile" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-600 hover:bg-slate-100 hover:text-slate-900 transition-colors font-medium">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
        Billing Profile
      </a>
'''

for file in templates:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<aside' in content and 'Transactions' in content and 'Billing Profile' not in content:
        # Insert before Transactions link
        content = content.replace('<a href="/transactions"', profile_link + '      <a href="/transactions"')
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
