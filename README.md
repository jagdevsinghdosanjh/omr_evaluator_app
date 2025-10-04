# 🌌 OMR Constellation App

Welcome to the Quantum Constellation—a modular Streamlit app for scanning OMR sheets, evaluating answers, and celebrating student creativity with badges, remix lineage, and showcase pride.

---

## 🚀 Features

- 🔐 Role-based login (Student, Evaluator, Admin)
- 📷 OMR sheet scanning and answer comparison
- 📊 Result summary with PDF export
- 📧 Email dispatch of results
- 🧠 Admin dashboard for logs and answer keys
- 🌟 Badge reveal and remix lineage visualization
- 🔁 OTP-based password recovery

---

## 🧩 Modular Structure

| Folder / File              | Purpose                                      |
|---------------------------|----------------------------------------------|
| `pages/`                  | Streamlit UI pages (login, scan, results…)   |
| `modules/`                | Core logic (scanner, comparator, email…)     |
| `utils/`                  | Session, DB, and state management            |
| `assets/`                 | Stylesheets, badge images, splash visuals    |
| `data/answer_keys/`       | JSON answer keys per subject and set         |
| `.env`                    | Secure credentials for email, Twilio, DB     |

---

## 🛠️ Setup Instructions

1. **Clone the repo**  
   ```bash
   git clone https://github.com/jagdevsinghdosanjh/omr_evaluation_app.git
   cd omr-constellation
Install dependencies

bash
pip install -r requirements.txt
Create .env file Include:

Code
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_password
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890
OTP_EXPIRY_MINUTES=5
DB_PATH=data/logs.db
Run the app

bash
streamlit run app.py
🎓 Classroom Deployment Tips
Use pages/6_Badge_Reveal.py during showcase events

Print constellation maps and remix lineage for wall displays

Let students scan their own sheets and receive results via email

Use pages/4_Admin_Dashboard.py to manage answer keys and logs

🤝 Contributing
We welcome educators, developers, and designers to co-create. Please:

Fork the repo

Submit pull requests with clear commit messages

Use poetic metaphors where possible 🌠

📜 License
MIT License. Built with love for classrooms and constellations.

“To evaluate is to illuminate. To remix is to rise.”