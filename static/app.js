// ============================================================
// NovaVPS — plain JS. Configure Cashfree below.
// ============================================================
const CASHFREE_MODE = "sandbox"; // "sandbox" | "production"

const PLANS = [
  {
    id: "pro", name: "Pro",
    tagline: "High-performance compute for growing applications.",
    priceMonthly: 19999, originalPriceMonthly: 25000, badge: "SAVE 20%", freeMonths: 0,
    features: ["32 vCPU AMD EPYC","128 GB DDR4 RAM","2 TB NVMe SSD","10 TB Bandwidth","Daily snapshots","Enterprise DDoS shield","Priority 24/7 support"],
    paymentSessionId: "", 
  },
  {
    id: "enterprise", name: "Enterprise", highlight: true,
    tagline: "Serious compute for high-traffic apps and critical workloads.",
    priceMonthly: 39865, originalPriceMonthly: 49999, badge: "FULLY MANAGED", freeMonths: 0,
    features: ["64 vCPU AMD EPYC","256 GB DDR4 RAM","4 TB NVMe SSD","Unmetered bandwidth","Hourly snapshots","99.99% uptime SLA","Dedicated manager"],
    paymentSessionId: "",
  },
  {
    id: "elite", name: "Elite",
    tagline: "Massive scale and performance for the largest databases.",
    priceMonthly: 79999, originalPriceMonthly: 99999, badge: "SAVE 20%", freeMonths: 0,
    features: ["128 vCPU AMD EPYC","512 GB DDR4 RAM","8 TB NVMe SSD","Unmetered bandwidth","Real-time replication","100% uptime SLA","White-glove support"],
    paymentSessionId: "",
  },
];

const FEATURES = [
  { icon: "⚡", image: "/static/images/feat_storage.png", title: "NVMe SSD storage", body: "Up to 20× faster than traditional SATA drives. Boot in seconds, deploy instantly." },
  { icon: "🛡", image: "/static/images/feat_security.png", title: "Enterprise DDoS shield", body: "Always-on Layer 3/4 mitigation and WAF protection included on every plan." },
  { icon: "🧠", image: "/static/images/feat_compute.png", title: "Dedicated compute", body: "AMD EPYC & Intel Xeon vCPUs with guaranteed clock speed — no noisy neighbors." },
  { icon: "🌍", image: "/static/images/feat_global.png", title: "12 global regions", body: "Deploy close to your users. Anycast networking with sub-30ms routing worldwide." },
  { icon: "💾", image: "/static/images/feat_backup.png", title: "Snapshots & backups", body: "One-click snapshots, automated daily backups, and 7-day retention on every VPS." },
  { icon: "🔑", image: "/static/images/feat_access.png", title: "Root access", body: "Full SSH root, choose your OS, and install anything. It's your machine." },
];

const FAQS = [
  { q: "How fast can I deploy a VPS?", a: "Most servers boot in under 60 seconds. Choose an OS, region, and plan — you'll get SSH access as soon as provisioning completes." },
  { q: "Which payment methods do you accept?", a: "Checkout is powered by Cashfree — UPI, credit/debit cards, net banking, and popular wallets." },
  { q: "Can I upgrade my plan later?", a: "Yes. Upgrades take a few minutes and require a quick reboot. Downgrades apply on the next billing cycle." },
  { q: "Do you offer refunds?", a: "30-day money-back guarantee on all VPS plans. If something isn't right, reach out and we'll make it good." },
  { q: "Is there an SLA?", a: "Every plan ships with 99.9% uptime SLA. Business tier steps up to 99.99% with service credits when we miss." },
];

// ------------------ Render features ------------------
const fc = document.getElementById("feature-carousel");
if (fc) {
  fc.innerHTML = FEATURES.map((f, i) => `
    <a href="#" class="group relative snap-center shrink-0 w-[85vw] md:w-[400px] lg:w-[600px] h-[350px] rounded-3xl overflow-hidden cursor-pointer shadow-lg hover:shadow-2xl transition-all">
      <div class="absolute inset-0 bg-black/50 z-10 group-hover:bg-black/40 transition-colors"></div>
      <img src="${f.image}" alt="${f.title}" class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" />
      <div class="absolute inset-0 z-20 flex flex-col justify-between p-8">
        <div class="self-start rounded bg-black/60 backdrop-blur-md px-3 py-1.5 text-lg font-bold tracking-wide text-white uppercase">${f.icon}</div>
        <div>
          <h3 class="text-2xl font-bold text-white leading-tight max-w-lg mb-3">${f.title}</h3>
          <p class="text-sm font-medium text-white/90 max-w-md mb-4 leading-relaxed">${f.body}</p>
          <div class="text-white font-bold text-xl group-hover:translate-x-2 transition-transform">→</div>
        </div>
      </div>
    </a>`).join("");

  const prevBtn = document.getElementById('carousel-prev');
  const nextBtn = document.getElementById('carousel-next');
  if (prevBtn && nextBtn) {
    prevBtn.addEventListener('click', () => {
      fc.scrollBy({ left: -window.innerWidth * 0.5, behavior: 'smooth' });
    });
    nextBtn.addEventListener('click', () => {
      fc.scrollBy({ left: window.innerWidth * 0.5, behavior: 'smooth' });
    });
  }
}

// ------------------ Render pricing ------------------
const pg = document.getElementById("pricing-grid");
if (pg) {
  pg.innerHTML = PLANS.map(p => {
    const savings = Math.round((1 - p.priceMonthly / p.originalPriceMonthly) * 100);
    return `
  <div class="relative rounded-3xl border ${p.highlight ? 'border-primary bg-white shadow-glow scale-[1.02]' : 'border-slate-200 bg-white'} p-8 flex flex-col">
    ${p.highlight ? `<span class="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-hero px-3 py-1 text-xs font-bold text-white shadow-elegant">★ MOST POPULAR</span>` : ""}
    ${p.badge ? `<span class="inline-flex w-fit rounded-full bg-emerald-100 px-2.5 py-1 text-[11px] font-bold text-emerald-700">${p.badge}</span>` : ""}
    <h3 class="mt-3 text-2xl font-bold">${p.name}</h3>
    <p class="mt-1 text-sm text-muted">${p.tagline}</p>
    <div class="mt-6 flex items-baseline gap-2">
      <span class="text-5xl font-bold">₹${p.priceMonthly}</span>
      <span class="text-muted">/month</span>
    </div>
    <div class="mt-1 flex items-center gap-2 text-sm">
      <span class="line-through text-muted">₹${p.originalPriceMonthly}</span>
      <span class="text-emerald-600 font-semibold">−${savings}%</span>
    </div>
    ${p.freeMonths ? `<p class="mt-1 text-xs text-primary font-semibold">+ ${p.freeMonths} FREE</p>` : ""}
    <ul class="mt-6 space-y-2.5 text-sm">
      ${p.features.map(f => `<li class="flex gap-2"><span class="text-emerald-500">✓</span>${f}</li>`).join("")}
    </ul>
    <button id="buy-btn-${p.id}" data-plan="${p.id}" class="buy mt-8 w-full rounded-lg ${p.highlight ? 'bg-hero text-white shadow-elegant' : 'bg-slate-100 text-slate-800 hover:bg-slate-200'} px-4 py-3 font-semibold transition hover:opacity-90">
      Buy ${p.name} →
    </button>
    <p class="mt-3 text-center text-xs text-muted">🛡 30-day money-back guarantee</p>
  </div>`;
  }).join("");
}

// ------------------ Render FAQ ------------------
const fl = document.getElementById("faq-list");
if (fl) {
  fl.innerHTML = FAQS.map((f,i) => `
  <details id="faq-item-${i}" class="group p-5" ${i===0?'open':''}>
    <summary id="faq-summary-${i}" class="flex cursor-pointer list-none items-center justify-between font-semibold">
      ${f.q}
      <span class="ml-4 text-primary transition group-open:rotate-45">＋</span>
    </summary>
    <p class="mt-3 text-sm text-muted">${f.a}</p>
  </details>`).join("");
}

const yearEl = document.getElementById("year");
if (yearEl) yearEl.textContent = new Date().getFullYear();

// ------------------ Cashfree checkout ------------------
document.querySelectorAll("button.buy").forEach(btn => {
  btn.addEventListener("click", async () => {
    const plan = PLANS.find(p => p.id === btn.dataset.plan);
    if (!plan.paymentSessionId) {
      alert("This plan doesn't have a Cashfree payment_session_id yet.\n\nGenerate one via the Cashfree dashboard/API and paste it into app.js → PLANS[" + plan.id + "].paymentSessionId.");
      return;
    }
    if (typeof Cashfree !== "function") {
      alert("Cashfree SDK not loaded yet. Please retry in a moment.");
      return;
    }
    try {
      btn.disabled = true;
      const original = btn.innerHTML;
      btn.innerHTML = "Opening checkout…";
      const cf = Cashfree({ mode: CASHFREE_MODE });
      const res = await cf.checkout({ paymentSessionId: plan.paymentSessionId, redirectTarget: "_self" });
      if (res && res.error) throw new Error(res.error.message || "Checkout failed");
      btn.innerHTML = original;
    } catch (e) {
      alert("Checkout error: " + (e.message || e));
    } finally {
      btn.disabled = false;
    }
  });
});

// ------------------ Terminal Animation ------------------
const terminalCommands = [
  { text: "$ avps deploy --plan pro --region blr1 --os ubuntu-24.04", type: "cmd" },
  { text: "✓ Provisioning 4 vCPU · 8 GB RAM · 100 GB NVMe", type: "out", delay: 800 },
  { text: "✓ Attaching dedicated IPv4 · enabling DDoS shield", type: "out", delay: 600 },
  { text: "✓ Boot completed in 41s", type: "out", delay: 1000 },
  { text: "", type: "out", delay: 200 },
  { text: "  ssh root@203.0.113.42", type: "out", delay: 100 },
  { text: "  https://console.AVPSSERVER.io/servers/edge-1", type: "out", delay: 100 }
];

async function typeTerminal() {
  const container = document.getElementById("terminal-content");
  if (!container) return;
  
  while (true) {
    container.innerHTML = "";
    
    for (const line of terminalCommands) {
      const lineEl = document.createElement("div");
      if (line.type === "cmd") {
        lineEl.className = "text-white font-semibold";
        container.appendChild(lineEl);
        for (let i = 0; i < line.text.length; i++) {
          lineEl.textContent += line.text[i];
          await new Promise(r => setTimeout(r, 30 + Math.random() * 30));
        }
      } else {
        await new Promise(r => setTimeout(r, line.delay || 500));
        lineEl.className = "text-white/90";
        lineEl.textContent = line.text;
        container.appendChild(lineEl);
      }
    }
    
    // Wait for 4 seconds before restarting the animation
    await new Promise(r => setTimeout(r, 4000));
  }
}

// Start animation slightly after load
setTimeout(typeTerminal, 600);

// ------------------ Login Modal Logic ------------------
const loginBtn = document.getElementById('nav-cta-login');
const loginModal = document.getElementById('login-modal');
const closeModalBtn = document.getElementById('close-modal');
const modalOverlay = document.getElementById('login-modal-overlay');
const loginForm = document.getElementById('login-form');
const loginError = document.getElementById('login-error');
const modalContent = document.getElementById('login-modal-content');

function openLoginModal() {
  if (loginModal) {
    loginModal.classList.remove('hidden');
    loginModal.classList.add('flex');
    // slight delay to allow display flex to apply before animating opacity
    setTimeout(() => {
      loginModal.classList.remove('opacity-0');
      modalContent.classList.remove('scale-95');
      modalContent.classList.add('scale-100');
    }, 10);
  }
}

function closeLoginModal() {
  if (loginModal) {
    loginModal.classList.add('opacity-0');
    modalContent.classList.remove('scale-100');
    modalContent.classList.add('scale-95');
    setTimeout(() => {
      loginModal.classList.add('hidden');
      loginModal.classList.remove('flex');
    }, 300);
  }
}

if (loginBtn) loginBtn.addEventListener('click', openLoginModal);
if (closeModalBtn) closeModalBtn.addEventListener('click', closeLoginModal);
if (modalOverlay) modalOverlay.addEventListener('click', closeLoginModal);

// Removed old static login form handling so Flask backend can take over
