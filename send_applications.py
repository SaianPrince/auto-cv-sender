"""
Automatic CV / Resume Email Sender
==================================
This script automates sending job application emails with CV attachments to a list of target companies.
It tracks successfully sent emails to prevent duplication and allows resuming if interrupted.
"""

import os
import smtplib
import time
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# Helper to load a local .env file if it exists (dependency-free)
def load_dotenv(dotenv_path=".env"):
    path = Path(dotenv_path)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("'\"")
                    os.environ[key] = val

# Load local environment variables if .env exists
load_dotenv()

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
# [IMPORTANT] Do not hardcode your password/email directly if uploading to GitHub!
# Instead, create a file named '.env' in this directory and define:
# EMAIL_USER=your_email@gmail.com
# EMAIL_PASS=your_app_password
# CV_PATH=C:/Path/To/Your/CV.pdf
#
# The script will automatically read them. Fallbacks are defined below:

GMAIL        = os.environ.get("EMAIL_USER", "your_email@gmail.com")
APP_PASSWORD = os.environ.get("EMAIL_PASS", "your_app_password")             # Google App Password (16 characters)
CV_PATH      = os.environ.get("CV_PATH", "path/to/your/CV.pdf")              # Path to your CV/Resume PDF file
DELAY_SEC    = int(os.environ.get("DELAY_SEC", 45))                          # Delay in seconds between emails (spam protection)
LOG_FILE     = os.environ.get("LOG_FILE", "sent_log.txt")                    # File to write execution logs
SENT_EMAILS_FILE = os.environ.get("SENT_EMAILS_FILE", "already_sent_emails.txt") # File to keep track of successfully sent emails
DRY_RUN      = True                                                          # Set to False to actually send emails. True = test run.
# ──────────────────────────────────────────────────────────────────────────────

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# --- TARGET EMAILS LIST ---
# Add or remove email addresses of the companies you want to apply to.
# The script will automatically remove duplicates and sort them.
EMAILS_LIST = [
    # Replace these with your target emails
    "info@themachineco.com",
    "info@motorasin.com.tr",
    "bilgi@miniskop.com.tr",
    "info@pera.software",
    "yazilim@dentsoft.com.tr",
    "sushico@sushico.com.tr",
    "info@gtech.com.tr",
    "info@signera.com",
    "iletisim@ledyazilim.com",
    "info@mobimyazilim.com",
    "info@faprika.com",
    "info@akyaosgb.com",
    "info@veriskop.com",
    "info@singingiant.com",
    "info@mepsistem.com.tr",
    "info@temteknik.com",
    "bilgi@narfon.com.tr",
    "info@karash.biz",
    "destek@niceye.com",
    "destek@webxt.com",
    "info@venokta.com.tr",
    "info@financebt.com",
    "info@magazanolsun.com",
    "info@rasstechnology.com",
    "info@skylandsoft.com",
    "info@rubusoft.com",
    "support@intranet.com.tr",
    "info@convoplus.com",
    "info@primesolutions.com.tr",
    "info@hinda.city",
    "partners@digitalpals.com", 
    "info@kvision.com.tr",
    "hello@viyatek.io",
    "connect@alpakagames.co",
    "info@moreum.com",
    "info@daprom.com",
    "info@sword-it.com",
    "bilgi@sanalogi.com",
    "destek@intimesolutions.net",
    "info@finartz.com",
    "info@bilgikurumsal.com",
    "info@fitekno.com",
    "info@smartin.com.tr",  # Sanitized to correct format from original info[ at ]smartin.com.tr
    "info@omnibus.dev",
    "info@trendbox.io",
    "info@futurino.com",
    "info@probar.com.tr",
    "info@create-4.com",
    "info@techsin.com.tr",
    "bilgi@meridyum.com",
    "info@ydrtech.com",
    "info@kepkur.com.tr",
    "info@innthebox.com",
]

# Deduplicate and sort emails list
EMAILS_LIST = sorted(list(set(EMAILS_LIST)))

def load_already_sent() -> set:
    """Loads already emailed addresses from log to prevent duplicate sending."""
    sent_path = Path(SENT_EMAILS_FILE)
    if sent_path.exists():
        with open(sent_path, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_as_sent(email: str):
    """Saves the email address to the already-sent tracking list."""
    with open(SENT_EMAILS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{email}\n")

def build_mail(target_email: str) -> MIMEMultipart:
    """Constructs the application email, including body and CV attachment."""
    msg = MIMEMultipart()
    # Replace 'Your Name' with your actual name
    msg["From"]    = f"Your Name <{GMAIL}>"
    msg["To"]      = target_email
    # Customize the Subject Line here
    msg["Subject"] = "Staj Başvurusu - Your Name"

    # --- EMAIL BODY TEMPLATE ---
    # Customize this text. You can use standard formatting.
    body = """Sayın Yetkili,

Necmettin Erbakan Üniversitesi Matematik ve Bilgisayar Bilimleri bölümü 4. sınıf öğrencisiyim. Yazılım geliştirme alanında pratik deneyim kazanmak amacıyla şirketinizde staj imkanı olup olmadığını öğrenmek için yazıyorum.

C++, Python, HTML, CSS, React, TypeScript ve FastAPI gibi teknolojilerle full-stack ve sistem programlama alanlarında kişisel projeler geliştirdim. Bunlar arasında bir C++ kod performans analiz aracı (React, FastAPI, PostgreSQL ve Docker ile), OpenCV tabanlı bir masaüstü fotoğraf düzenleme uygulaması ve C++ ile Python arasında TCP soket iletişimi kullanan bir otonom araç simülasyonu yer almaktadır. Bilgisayarlı görü, otonom sistemler ve full-stack web geliştirme alanlarına özellikle ilgi duyuyorum.

Özgeçmişimi ekte bulabilirsiniz. Ekibinize katkı sağlayabileceğim bir staj fırsatı için değerlendirmenizi rica eder, geri dönüşünüzü sabırsızlıkla beklerim.

İlginiz için şimdiden teşekkür ederim.

Saygılarımla,
Your Name
Your Phone Number
Your LinkedIn Profile URL
Your GitHub Profile URL
"""

    msg.attach(MIMEText(body, "plain", "utf-8"))

    # Attach the CV PDF
    cv_path = Path(CV_PATH)
    if cv_path.exists():
        with open(cv_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{cv_path.name}"')
        msg.attach(part)
    else:
        logging.warning(f"CV not found at target path: {CV_PATH}")

    return msg

def send(msg: MIMEMultipart, to: str):
    """Establishes connection to Gmail SMTP server and sends the email."""
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL, APP_PASSWORD)
        server.send_message(msg)

def safe_print(text: str):
    """Prints text safely to console, handling Unicode encoding issues on Windows."""
    import sys
    try:
        print(text)
    except UnicodeEncodeError:
        encoding = sys.stdout.encoding or "utf-8"
        print(text.encode(encoding, errors="replace").decode(encoding))

def main():
    already_sent = load_already_sent()
    todo_list = [email for email in EMAILS_LIST if email not in already_sent]

    run_prefix = "[DRY RUN] " if DRY_RUN else ""
    logging.info(f"{run_prefix}Total of {len(todo_list)} new companies to email. (Skipped {len(already_sent)} already sent emails)\n")

    sent, failed, skipped = 0, 0, 0

    for i, email in enumerate(todo_list, 1):
        if not email or "@" not in email:
            logging.warning(f"[{i}] SKIPPED (Invalid email) → {email}")
            skipped += 1
            continue

        try:
            msg = build_mail(email)

            if DRY_RUN:
                logging.info(f"[{i}] [DRY RUN] → <{email}>")
                safe_print(f"\n{'-'*60}")
                safe_print(f"SUBJECT  : {msg['Subject']}")
                safe_print(f"RECIPIENT: {email}")
                safe_print('-'*60)
            else:
                send(msg, email)
                logging.info(f"[{i}] ✓ SENT → <{email}>")
                save_as_sent(email)
                sent += 1
                if i < len(todo_list):
                    logging.info(f"    Waiting {DELAY_SEC} seconds...")
                    time.sleep(DELAY_SEC)

        except Exception as e:
            logging.error(f"[{i}] ✗ ERROR → <{email}> | {e}")
            failed += 1

    safe_print(f"\n{'='*60}")
    safe_print(f"{'[DRY RUN COMPLETED]' if DRY_RUN else 'COMPLETED'}")
    safe_print(f"Sent   : {sent}")
    safe_print(f"Failed : {failed}")
    safe_print(f"Skipped: {skipped}")
    safe_print(f"Log file saved to: {LOG_FILE}")
    if DRY_RUN:
        safe_print("\nTo actually send the emails, change DRY_RUN = False in the script.")
    safe_print("="*60)

if __name__ == "__main__":
    main()
