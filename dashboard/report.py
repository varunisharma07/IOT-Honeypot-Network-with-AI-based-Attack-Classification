from reportlab.pdfgen import canvas
import sqlite3


conn = sqlite3.connect("database/honeypot.db")
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM attacks")
total = cur.fetchone()[0]

pdf = canvas.Canvas("security_report.pdf")

pdf.drawString(
    100,
    750,
    "IoT Honeypot Security Report"
)

pdf.drawString(
    100,
    700,
    f"Total Attacks Detected: {total}"
)

pdf.save()

print("Report Generated")

