# VastraVibe

A Django fashion-shopping web application inspired by modern fashion marketplaces.

## Planned modules
- Product discovery: categories, search, filters, sorting, product details
- Customer accounts: registration, login, email verification, profile, addresses
- Shopping: wishlist, size-aware cart, coupons, checkout
- Orders: COD checkout, confirmation email, order history, tracking, cancellation, returns/exchanges
- Admin: products, inventory, orders, coupons, banners, reviews and sales reporting
- Later extensions: online payments, loyalty, referrals, recommendations and notifications

## Local setup
1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and configure database/email settings.
4. Run `python manage.py migrate` then `python manage.py runserver`.

Configure MySQL before using production data; never commit credentials.
