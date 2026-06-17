# Auto CV Sender 🚀

An easy-to-use, zero-dependency Python script designed to automate sending job or internship application emails with resume/CV attachments. It features duplicate prevention, custom anti-spam delays, logging, and test run simulation.

---

## Key Features

- **Zero-Dependency**: Built entirely using Python's standard library. No `pip install` required!
- **State Persistence (Resumable)**: Tracks successfully sent emails in a text file. If the script is stopped or crashes, it automatically skips already contacted companies when restarted.
- **Dry-Run Mode (Simulation)**: Verify email subject lines, recipients, and attachments in test mode before sending actual emails.
- **Spam Protection**: Custom delay interval between each email to prevent SMTP rate limits and spam filters.
- **Security-First**: Support for local `.env` files to prevent committing sensitive email passwords directly to GitHub.

---

## Directory Structure

```text
auto-cv-sender/
├── .gitignore               # Prevents tracking logs, credentials, and cache files
├── .env.example             # Sample template for configuration variables
├── send_applications.py     # Main Python automation script
└── README.md                # Project documentation (this file)
```

---

## Step-by-Step Setup

### Step 1: Clone or Copy the Repository
Download this folder or clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/auto-cv-sender.git
cd auto-cv-sender
```

### Step 2: Get a Gmail App Password
Gmail does not allow standard passwords for SMTP login unless you generate a specific App Password:
1. Go to your **[Google Account Console](https://myaccount.google.com/)**.
2. Navigate to **Security** on the left menu.
3. Under *How you sign in to Google*, make sure **2-Step Verification** is enabled.
4. Click on **2-Step Verification**, scroll to the bottom, and select **App passwords**.
5. Select or type a custom app name (e.g. `AutoCVSender`), then click **Create**.
6. Copy the generated **16-character code** (this is your `EMAIL_PASS`).

### Step 3: Configure Environment Variables
You have two ways to configure the script. Using a `.env` file is the safest way to avoid pushing passwords to GitHub.

#### Option A: Using a `.env` file (Recommended)
1. Copy the `.env.example` file and rename it to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your credentials:
   ```env
   EMAIL_USER=your_gmail_address@gmail.com
   EMAIL_PASS=abcd-efgh-ijkl-mnop
   CV_PATH=C:/Path/To/Your/CV.pdf
   DELAY_SEC=45
   ```

#### Option B: Directly in the Script
Open [send_applications.py](send_applications.py) and modify the fallback values under the `─── CONFIGURATION ───` section:
```python
GMAIL        = "your_gmail_address@gmail.com"
APP_PASSWORD = "abcd-efgh-ijkl-mnop"
CV_PATH      = "C:/Path/To/Your/CV.pdf"
```

### Step 4: Customize the Email Content & Recipient List
1. **Target Companies**: In [send_applications.py](send_applications.py), scroll down to the `EMAILS_LIST` list and add your target email addresses.
2. **Email Subject & Body**: Customize the `msg["Subject"]` and the `body` string inside the `build_mail` function to suit your application.

---

## Running the Script

### 1. Run in Simulation (Dry Run) Mode
By default, the script has `DRY_RUN = True` enabled. This outputs all steps and email subjects to your terminal and logs without sending any actual emails:
```bash
python send_applications.py
```
Check the output to make sure formatting, paths, and email list look correct.

### 2. Live Run
Once you are confident everything is set up correctly:
1. Open [send_applications.py](send_applications.py)
2. Locate the line `DRY_RUN = True`
3. Change it to `DRY_RUN = False`
4. Run the script:
   ```bash
   python send_applications.py
   ```

---

## Log & Tracking Files
Once run, the script automatically generates two files (both ignored by `.gitignore` so they remain private to you):
- `sent_log.txt`: Contains timestamped logging of successful sends, skipped emails, or errors.
- `already_sent_emails.txt`: A simple list of emails that were successfully emailed. The script reads this file on launch to skip them.

---

## Troubleshooting

- **`SMTPAuthenticationError`**: Double-check your email and App Password. Make sure 2-Step Verification is enabled and that you are using a 16-character Gmail App Password, not your normal password.
- **`CV not found at target path`**: Make sure the file path to your CV PDF is absolute or relative, and uses forward slashes `/` (even on Windows). Example: `C:/Users/Username/Documents/MyCV.pdf`.
