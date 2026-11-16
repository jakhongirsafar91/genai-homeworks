# L09 — Check

I checked every number against `orders.csv`, recomputing independently with pandas.

## Thing #1 — Deck (`thing1_deck.md`)
1. **Numbers and facts right?** Yes, all match the source: 1,220 orders, 1,110 completed, revenue $8,590.81, Cakes 42.0%, Saturday 25.5%, Fri–Sun 61.7%, channel shares 52.4%/38.4%/9.3%, 110 lost orders = $618.23. The deck uses the corrected (completed-only) numbers from the dashboard fix.
2. **What did Claude make up?** I asked "what did you invent?". Answer: (a) the *reasons* behind patterns (why Saturday peaks, why Wednesday is weak) are not in the data, so slide 5 labels them as hypotheses; (b) the offer ideas are my suggestions, not data; (c) the **data itself is simulated** by me, not a real bakery's.
3. **Personal data?** None. Customers are codes (C001–C140), no names, emails, phones or addresses.

## Thing #2 — Dashboard (`dashboard.html`)
1. **Numbers and facts right?** **v1 was wrong.** It summed all 1,220 orders: revenue $9,209.04, 1,220 orders, average $7.55. Source check: 84 cancelled and 26 refunded orders were inside. Correct: $8,590.81, 1,110 orders, average $7.74. v1 overstated revenue by 7.2%. Fixed in v2 (see prompts.md).
   **Second finding, not fixed:** the first week (27 Jul) has only 2 days of data and the last (26 Oct) has 6, so those bars look like dips but are partial weeks.
2. **What did Claude make up?** Nothing in the numbers; every figure is computed from the file. Invented or chosen by me: the simulated data, the week grouping (Monday start), colours and layout.
3. **Personal data?** None, same as above. Safe to share the link.
