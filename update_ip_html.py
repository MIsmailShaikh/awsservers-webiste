import re

with open('d:/project_vps/templates/static-ips.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the ID heading to include nickname and edit button
old_heading = '''                <h3 class="text-lg font-bold text-slate-900 tracking-tight">ID: {{ ip.id }}</h3>
                <p class="text-xs text-slate-500 font-medium mt-0.5">{{ ip.type }}</p>'''

new_heading = '''                <h3 class="text-lg font-bold text-slate-900 tracking-tight flex items-center gap-2">
                  ID: {{ ip.id }}
                  <button onclick="editNickname('{{ ip.id }}', '{{ ip.nickname or '' }}')" class="text-slate-400 hover:text-primary transition-colors" title="Edit Nickname">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                  </button>
                </h3>
                <p class="text-xs text-slate-500 font-medium mt-0.5">
                  {{ ip.type }} {% if ip.nickname %}&bull; <strong class="text-primary">{{ ip.nickname }}</strong>{% endif %}
                </p>'''

content = content.replace(old_heading, new_heading)

# Add the script to the end of the file before </body>
script_tag = '''
  <script>
    async function editNickname(ipId, currentNickname) {
        const nickname = prompt("Enter a nickname for IP " + ipId + ":", currentNickname);
        if (nickname !== null) {
            try {
                const response = await fetch('/update-ip-nickname', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ ip_id: ipId, nickname: nickname })
                });
                
                if (response.ok) {
                    window.location.reload();
                } else {
                    alert("Failed to save nickname.");
                }
            } catch (error) {
                console.error("Error saving nickname:", error);
                alert("Failed to save nickname. Please try again.");
            }
        }
    }
  </script>
</body>'''

content = content.replace('</body>', script_tag)

with open('d:/project_vps/templates/static-ips.html', 'w', encoding='utf-8') as f:
    f.write(content)
