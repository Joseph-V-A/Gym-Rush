# 🏋️ Gym Rush

> A full-stack gym management web application built with Django — connecting gym owners, instructors, and members on a single platform.

---

## 📌 Overview

Gym Rush is a multi-role web application that streamlines the day-to-day operations of a gym. It supports four distinct user roles — **Admin**, **Gym Owner**, **Instructor**, and **Member** — each with their own dedicated dashboard and features.

---

## ✨ Features

### 👤 Member
- Register and log in securely
- Browse and search for nearby gyms
- View gym details, equipment, ratings, and pricing
- Book monthly or yearly gym memberships
- Book training slots with instructors
- View personal workout plans assigned by instructors
- Rate and review gyms
- Send and receive feedback messages

### 🏢 Gym Owner
- Register gym with documents and equipment details
- Set monthly membership rates
- Manage instructors — post job offers, accept/reject applications
- Create and manage training slots
- Track instructor attendance and approve/reject leave requests
- View member bookings and subscription status

### 🧑‍💼 Instructor
- Register with CV and documents
- Apply to gyms for job positions
- View assigned training slots and substitution slots
- Mark and track attendance
- Submit leave requests to gym owners
- Assign and update workout plans for members
- Add remarks to member progress

### 🔐 Admin
- Approve or reject gym and instructor registrations
- Manage gym equipment catalog with images
- Monitor platform-wide users, gyms, and instructors
- Send feedback to any user role

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django 4.1 |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Email | Gmail SMTP |
| Auth | Custom password hashing via Django |

---

## 📁 Project Structure

```
GymSystem/
│
├── Admin/          # Admin panel — equipment & user approvals
├── Guest/          # Public pages & shared registration models
├── Gym/            # Gym core logic — slots, bookings, attendance, leaves
├── Instructor/     # Instructor views and job management
├── User/           # Member views and workout tracking
├── GymSystem/      # Project settings, URLs, WSGI/ASGI
├── templates/      # HTML templates
├── static/         # CSS, JS, fonts, icons
├── manage.py
└── .env.example    # Environment variable template
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8+
- pip

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/gym-rush.git
cd gym-rush
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

> 💡 For `EMAIL_HOST_PASSWORD`, use a [Gmail App Password](https://myaccount.google.com/apppasswords), not your regular Gmail password.

### 5. Apply migrations
```bash
python manage.py migrate
```

### 6. Create a superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 👥 User Roles & Login

| Role | How to Access |
|---|---|
| Admin | `/admin` or via superuser login |
| Gym Owner | Register as a gym and wait for admin approval |
| Instructor | Register as an instructor and wait for admin approval |
| Member | Register directly and start browsing gyms |

---

## 📸 Screenshots

> ![Home Page](./screenshots/home.png)

---

## 🔒 Security Notes

- Passwords are hashed using Django's `make_password`
- Sensitive credentials are stored in `.env` (never committed to Git)
- `db.sqlite3` is excluded from the repository
- CSRF protection is enabled via Django middleware

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@Joseph-V-A](https://github.com/Joseph-V-A)
