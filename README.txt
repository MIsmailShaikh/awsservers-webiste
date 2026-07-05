NovaVPS — static HTML/CSS/JS build
====================================

Files:
- index.html   Single-page site (Tailwind via CDN, Google Fonts, Cashfree SDK)
- app.js       Plans, features, FAQ data + Cashfree checkout wiring

How to run:
  Just open index.html in a browser. No build step. Or host any static server:
    npx serve .
    python3 -m http.server

Cashfree setup:
1. Open app.js
2. Set CASHFREE_MODE = "sandbox" or "production"
3. For each plan in PLANS[], paste a payment_session_id generated via
   Cashfree dashboard/API into the `paymentSessionId` field.

That's it. The "Buy" buttons will launch Cashfree's hosted checkout.
