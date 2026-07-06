import glob

old_profile_btn = """        <button class="w-9 h-9 flex items-center justify-center rounded-full border border-slate-200 text-slate-600 hover:bg-slate-50 transition-colors">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        </button>"""

new_profile_btn = """        <div class="relative group">
          <button class="w-9 h-9 flex items-center justify-center rounded-full border border-slate-200 text-slate-600 hover:bg-slate-50 transition-colors focus:outline-none">
            <div class="w-9 h-9 rounded-full bg-indigo-100 flex items-center justify-center text-primary font-bold text-sm border border-indigo-200 overflow-hidden shadow-sm transition-all">
                MS
            </div>
          </button>
          <div class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg border border-slate-100 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
            <div class="px-4 py-3 border-b border-slate-100">
              <p class="text-sm font-bold text-slate-900">Mohammed Ismail Shaikh</p>
              <p class="text-xs text-slate-500 truncate">ismailzst643</p>
            </div>
            <div class="p-2">
              <a href="/logout" class="flex items-center gap-2 px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg font-medium transition-colors">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                Logout
              </a>
            </div>
          </div>
        </div>"""

jd_btn = """        <div class="w-9 h-9 rounded-full bg-indigo-100 flex items-center justify-center text-primary font-bold text-sm border border-indigo-200 overflow-hidden cursor-pointer shadow-sm hover:ring-2 hover:ring-primary/20 transition-all">
            <a href="/logout">JD</a>
        </div>"""

templates = glob.glob('templates/*.html')
for template in templates:
    with open(template, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace JD button with empty string
    content = content.replace(jd_btn, "")
    
    # Replace profile button with dropdown
    content = content.replace(old_profile_btn, new_profile_btn)
    
    with open(template, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Updated HTML templates.")
