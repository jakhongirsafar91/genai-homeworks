# L09 — Prompts

## Thing #1 — Deck (project topic)
```
Make a 5-slide deck for the owner of a small bakery: "Where does our revenue come from?"
Use only the attached orders.csv (Aug–Oct 2026). Slides: question; data and method;
what earns the money (category, weekday, channel); what we lose; next steps.
One idea per slide, numbers must come from the file. Do not invent causes:
mark any recommendation as a hypothesis.
```

## Thing #2 — Dashboard (from the same data)
```
I attached orders.csv (anonymised: customers are codes). Build a dashboard as an artifact.
Ask yourself what matters most: show total revenue, orders, average order, and revenue
by category, weekday, channel and week. Light and dark mode friendly.
```
Result v1: `dashboard_v1_before_fix.html`

## The one precise fix (Thing #2)
```
What's wrong: revenue, orders and average order include cancelled and refunded orders,
so the dashboard overstates revenue.
What to change: count only orders with status "completed" in all KPIs and charts,
and say so in the subtitle.
What to keep: the layout, the five panels, colours, and light/dark mode.
```
Result v2: `dashboard.html`
