import sys
from pdfminer.high_level import extract_text
from classes.invoice_class import Invoice
import pandas as pd

# Check correct usage
if len(sys.argv) != 2:
	print("[ERROR]: Usage: ./invoicer PATH_TO_INVOICE")
	exit(1)

# # Store invoice path
# # FIXME: implement file uploading when frontend is done
invoice_path = sys.argv[1]

invoice = Invoice(invoice_path)
data = invoice.parse()
print(data)