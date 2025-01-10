
# SkillFrame 🚀

SkillFrame is a Django-powered platform for tech enthusiasts to showcase their skills, manage projects, write blogs, and organize tasks. It’s an all-in-one responsive, animated, and feature-rich portfolio application for everything tech-related: development, cybersecurity, Web3, and more.

---

## 🌟 Features

### User Management
- **Authentication**: Sign up, log in, and secure your account with Django's robust authentication system.
- **Profiles**: Showcase skills, projects, and expertise with a personalized profile.

### Project & Portfolio Management
- Upload, update, and display projects with tags, descriptions, and media files.
- Categorize skills in domains like development, hacking, Web3, and more.

### Task Management
- Integrated **To-Do List** to help users track and organize goals.

### Blogging
- Write, edit, and publish blogs with an intuitive editor.
- Share knowledge and engage with the community.

### Dynamic Animations & Responsiveness
- Modern tech-inspired animations for an engaging user experience.
- Fully responsive design for seamless access on any device.

---

## 💻 Tech Stack

### Backend
- **Django**: Core framework.
- **Django REST Framework (DRF)**: For building APIs.
- **SQLite** or **PostgreSQL**: Database options.

### Frontend
- **HTML5**, **CSS3**, **JavaScript**
- **Bootstrap** for responsive design and components.

### Features and Integrations
- **Authentication**: Django's built-in user management system.
- **Media Uploads**: Handled via `django-storages` or local storage.
- **Rich Text Editing**: Django CKEditor for blogs.

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.9+**
- **pip** (Python package manager)
- Virtual environment (optional but recommended)
- SQLite (default) or PostgreSQL database

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/skillframe.git
   cd skillframe
   ```

2. **Create and activate a virtual environment**:
   - On macOS/Linux:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory with the following:
   ```plaintext
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3  # Or your PostgreSQL connection string
   ```

5. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:8000`.

---

## 📁 Folder Structure

Here's an overview of the project structure:

```
SkillFrame/
├── skillframe/         # Core project settings and configurations
├── users/              # User management app
├── projects/           # Portfolio and project management app
├── blogs/              # Blogging feature app
├── tasks/              # To-Do list app
├── static/             # Static files (CSS, JavaScript, Images)
├── templates/          # HTML templates
├── requirements.txt    # Python dependencies
└── .env                # Environment variables
```

---

## ✨ Contribution Guidelines

We welcome contributions from the community! If you have ideas or would like to fix bugs, feel free to fork the repo and open a pull request.

### Steps to Contribute:
1. Fork the repository.
2. Create a new branch for your feature/bugfix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request and describe your changes.

---

## 📜 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
