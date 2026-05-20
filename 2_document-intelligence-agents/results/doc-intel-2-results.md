(.venv) (base) gabrrodriguez@US-L47X4HJX75 2_document-intelligence-agents % python doc-intelligence-2.py ./docs/single-invoice.pdf
Extracted fields: 
 invoice_number: INVOICE
 invoice_date:  
 total_amount: Due: $126.25

 --------

< See image/doc-intel-2results >

 Looking at the results vs. the invoice, I can see three issues:

invoice_number: INVOICE — the SCHEMA keywords don't include plain "invoice", so it fuzzy-matched the header but returned the wrong token
invoice_date: (empty) — the label on the invoice is just "Date:", none of the current keywords match it
total_amount: Due: $126.25 — correct value but "Due:" prefix isn't stripped because it's in the middle of the value string, not at the edge
Two fixes needed: update the SCHEMA keywords to match the actual labels in this invoice, and add regex stripping to remove leading label-word prefixes from extracted values.

----------

Three changes made to doc-intelligence-2-fix.py:

1. import re added at the top
2. SCHEMA keywords — added "invoice" to invoice_number, "date" to invoice_date, and "total" to total_amount so they match the shorter labels this invoice actually uses
3. Value cleaning — replaced .strip(": ") with re.sub(r'^[A-Za-z\s]+:\s*', '', ...) in both pass1 and pass2, which strips a leading word-colon prefix like "Due: " from the middle of an extracted value


----------
