 # 🦈 BizVest — Startup Investment Portal

Welcome to *BizVest*, a Django-based web platform inspired by the popular startup investment show. This application connects startups and investors on a single platform where users can pitch, invest, and manage startup portfolios efficiently.

## 🔧 Features

- 📝 User authentication (Register/Login/Logout)
- 🧑‍💼 Separate dashboards for Startups & Investors
- 💰 Investment deal management
- 📊 Analytics and insights per sector
- 👤 Profile view and session-based user roles
- 📄 Responsive UI using Tailwind CSS

---

## 🛠 Tech Stack

### 💻 Backend
- *Python 3.x*
- *Django 4.x*
- Django ORM (SQL handling)

### 🎨 Frontend
- *HTML5 & Jinja2 (Django Templates)*
- *Tailwind CSS* (via django-tailwind)
- *SVG Icons*

### 🗃 Database
- Default: *SQLite3*
- (Easily switchable to PostgreSQL/MySQL)
- We used MySQL
---

## 📂 Project Structure (Simplified)
![image](https://github.com/user-attachments/assets/32173919-c62e-4868-82fe-712fa78a889b)


---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Siddharththakur3617/Shark_Tank.git
cd Shark_Tank
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Start Development Server
```bash
python manage.py runserver
```

---

## 👤 User Roles

Startups and investors alike can leverage a dynamic platform designed to streamline the investment process.

### 🚀 Startups can:
- Register and create detailed startup profiles
- Craft compelling pitch descriptions to attract investors
- Monitor their own investments and funding received
- Track performance metrics to gauge business success

### 💼 Investors can:
- Explore a wide variety of startup opportunities
- Make informed investment decisions based on:
  - Pitch quality
  - Valuation
  - Sector insights
- View and manage their investment portfolio
- Analyze total investments categorized by sector

This fosters a seamless, data-driven ecosystem for both sides to connect, collaborate, and grow together.

---

### 🔮 Future Plans

We are actively working on improving *Shark Tank*. In the upcoming versions, we plan to:

- 🎨 Enhance and modernize the *frontend UI/UX* with improved animations, transitions, and a more polished design.
- 📱 Make the platform fully *mobile-responsive* and accessible across all devices.
- 🔐 Implement more secure and scalable *authentication and authorization*, including role-based permissions.
- 💬 Add interactive features like:
  - Startup pitch ratings and user reviews
  - Real-time chat between investors and startups
  - Notifications for investment updates and profile views
- 📊 Include insightful *dashboard analytics* and visualizations.
- 🌍 Add *multi-language support* for global accessibility.
- ⚙ Improve performance and backend scalability for larger datasets.

We’re excited about what’s coming next. Stay tuned for updates!
