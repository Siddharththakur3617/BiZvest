# 🦈 BiZvest — Startup Investment Portal

**BiZvest** is a Django-based startup-investor matchmaking platform inspired by a famous TV show. It brings **startups** and **investors** together, enabling streamlined offer creation, investment tracking, and deal finalization, all managed through role-based dashboards.

---

## 🚀 Features

- 🔐 **Authentication System**  
  Secure login system for:
  - Admin 
  - Startup users
  - Investor users

- 🧑‍💼 **Startups**
  - Register and log in
  - Create funding offers
  - View and manage incoming deals

- 💰 **Investors**
  - Register and log in
  - View startup offers
  - Accept offers to create deals

- 🛠 **Admin Panel**
  - View and delete users
  - View all deals across the platform
  - Add new sectors
  - Monitor platform activity

- 📊 **Sectors View**
  - Sector-wise filtering of both investors and startups
  - Sector-interest modeling via `Choices` model

---


## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Siddharththakur3617/BiZvest.git
cd BiZvest
```

### 2. Create and activate a virtual environment

```bash
python -m venv env
source env/bin/activate      # Windows: env\Scripts\activate
```

### 3. Install the dependencies
```bash
pip install -r requirement.txt
```

### 4. Apply migrations and create superuser (optional)
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run the development server
```bash
python manage.py runserver
```

---


## 🧠 Data Model

### Core Models:

- **AppUser**: Auth system (linked to either investor or startup)
- **Startup**: Startup info + sector
- **Investor**: Investor info
- **Deals**: Finalized agreements between startups and investors
- **Offers**: Funding requests created by startups
- **Sector**: Domain/category (e.g., FinTech, EdTech)
- **Choices**: Investor interest in specific sectors

---

## ✨ Interface of the model

![IMG-20250703-WA0003 1](https://github.com/user-attachments/assets/08e97332-2301-46b8-abad-ed54b2e774a1)

---

## 📦 Tech Stack

- **Backend**: Django  
- **Frontend**: HTML, Tailwind CSS  
- **Database**: MySQL  
- **Logging**: Python `logging` for admin actions

---

## 📈 Future Enhancements

Here are some features planned for future versions of BiZvest:

- ✅ Add better security features like email confirmation
- 📊 Show insights like which sectors are getting the most investments
- 🔍 Improve filtering to find the best startups or investors easily
- 💬 Allow messaging between startups and investors
- 🔄 Allow connection with other apps in the future
- 🧪 Add automatic checks to make sure everything works correctly
- 👥 Let teams manage their startup or investor profile together
