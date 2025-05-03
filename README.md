# Holiday Club  
https://your-holiday-club-d5454424f4de.herokuapp.com/  
**Author**: Aleksandar Husagic  

Holiday Club is a community-driven Flask web application where travelers register, share, and explore holiday stories. It demonstrates a fully relational design (users ↔ stories) and covers manual test procedures for functionality, usability, responsiveness, and data management.

---

## Table of Contents
1. [Project Description](#project-description)  
2. [User Stories](#user-stories)  
3. [Features](#features)  
4. [Technologies](#technologies)  
5. [Database Structure & 1.4 Criterion](#database-structure--14-criterion)  
6. [Manual Testing & 1.5 Criterion](#manual-testing--15-criterion)  
7. [Code Validation](#code-validation)  
8. [Deployment](#deployment)  
9. [Installation & Usage (Local)](#installation--usage-local)  
10. [License](#license)  

---

## Project Description

Holiday Club allows registered users to:

- **View** all holiday stories in a responsive grid.  
- **Read** each story in detail (with images).  
- **Add** a new holiday story.  
- **Edit** their own stories.  
- **Delete** their own stories.  

It fosters a collaborative environment for sharing travel experiences and tips.

---

## User Stories

1. **Visitor**: See a list of travel stories to discover new destinations.  
2. **Contributor**: Register and add a travel story for others to read.  
3. **Returning User**: Edit my previously posted story to correct or add details.  
4. **Account Owner**: Delete my own story if I choose.  
5. **Inquirer**: Use the contact form to send feedback or questions.

---

## Features

- **Authentication**: Register, log in, log out.  
- **Authorization**: Only story authors may edit/delete their own entries.  
- **CRUD**: Create, read, update, and delete stories.  
- **Responsive Design**: Adapts to mobile and desktop, includes a hamburger menu.  
- **Dark-Mode Toggle**: Switch between light and dark themes.  
- **Flash Messages**: Success/error feedback after every action.  
- **Seed Data**: A default user and sample stories are inserted on first run.  
- **Contact Form**: Visitors may send inquiries to the admin.

---

## Technologies

- **Backend**: Python, Flask  
- **Database**: SQLite (via `sqlite3`)  
- **Templating**: Jinja2 (HTML)  
- **Styling**: CSS3, minimal JavaScript for toggles  
- **Wsgi Server**: Gunicorn  
- **Hosting**: Heroku  

---

## Database Structure 

relational schema that satisfies criteria 1.4:

- **`users`**  
  - `id` INTEGER PK,  
  - `username` TEXT UNIQUE,  
  - `email` TEXT,  
  - `password_hash` TEXT  

- **`stories`**  
  - `id` INTEGER PK,  
  - `user_id` INTEGER FK → `users.id`,  
  - `location` TEXT,  
  - `story_text` TEXT  

Each story record belongs to exactly one user. I seed a `default_user` on first run and link sample stories, demonstrating the one-to-many relationship in practice.

---

## Manual Testing 

Criteria 1.5 is met through the following manual test plan, covering functionality, usability, responsiveness, and data integrity.

| Area                       | Test Case                  | Steps                                                                                              | Expected Result                                                                                       |
|----------------------------|----------------------------|----------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| **Home Page**              | Load Home                  | 1. Navigate to `/`                                                                                 | Hero banner, “View Stories” button, navbar links appear.                                              |
| **Navigation**             | Nav Links                  | 1. Click About, Contact, Stories, Login/Register                                                   | Each page loads with correct content.                                                                 |
| **About Page**             | Content & Layout           | 1. Go to `/about`                                                                                  | Mission, future plans, quotes grid render correctly.                                                  |
| **Contact Form**           | Successful Submission      | 1. Go to `/contact`<br>2. Fill Name, Email, Message<br>3. Submit                                   | Flash “Thank you for your message…”.                                                                   |
|                            | Validation Error           | 1. Submit empty form                                                                               | Flash error about required fields.                                                                    |
| **Authentication**         | Register New User          | 1. `/register` → valid data → Submit                                                               | Flash “Registration successful!”, redirect to login.                                                  |
|                            | Duplicate Username         | 1. Register same username again                                                                     | Flash “Username already taken.”                                                                        |
|                            | Login / Logout             | 1. `/login` → correct creds → Home, navbar shows “Hi, USER”<br>2. Click Logout                       | Flash “Welcome, USER!” then “You’ve been logged out.”                                                  |
|                            | Invalid Credentials        | 1. `/login` → wrong creds                                                                          | Flash “Invalid credentials.”                                                                          |
| **View Stories**           | List Seeded Stories        | 1. `/viewstory`                                                                                   | Stories display in grid with location, author, excerpt, “Read More.”                                   |
| **Story Detail**           | View Single Story          | 1. Click “Read More”                                                                               | Detail page shows full text, author, images, Edit/Delete if owner.                                     |
|                            | 404 Handling               | 1. `/story/9999`                                                                                   | Flash “Story not found!”, redirect to `/viewstory`.                                                   |
| **Add Story**              | Successful Add             | 1. Login<br>2. `/addstory` → fill fields → Submit                                                  | Flash “Story added successfully!”, story appears in list.                                             |
|                            | Validation Error           | 1. Submit `/addstory` empty                                                                        | Flash “Please fill in all fields.”                                                                     |
|                            | Unauthorized Redirect      | 1. While logged out, request `/addstory`                                                           | Redirect to `/login` with flash “Please log in first.”                                                 |
| **Edit Story**             | Successful Edit            | 1. Login as owner<br>2. `/editstory/<id>` → change → Submit                                        | Flash “Story updated successfully!”, changes show.                                                    |
|                            | Validation Error           | 1. `/editstory/<id>` empty                                                                         | Flash “Please fill out all fields.”                                                                    |
|                            | Unauthorized Access        | 1. Login as different user<br>2. Access `/editstory/<other_id>`                                     | Flash “You can only modify your own stories.”                                                          |
| **Delete Story**           | Successful Delete          | 1. Login as owner<br>2. `/deletestory/<id>` → confirm                                              | Flash “Story deleted successfully!”, story removed.                                                   |
|                            | Unauthorized Access        | 1. Login as different user<br>2. Delete another’s story                                            | Flash “You can only delete your own stories.”                                                          |
| **Responsive Layout**      | Mobile View                | 1. Resize < 768px or DevTools mobile emulation                                                     | Navbar collapses, grids adjust to 1–2 columns.                                                         |
| **Dark Mode**              | Toggle Dark Mode           | 1. Click 🌙 button                                                                                 | Dark-mode styles apply site-wide.                                                                      |
| **Data Persistence**       | Refresh & Re-login         | 1. Add/Edit/Delete → refresh → logout/login                                                         | All changes persist correctly.                                                                         |

---

## Code Validation

- **HTML/CSS** validated via [W3C Markup Validator](https://validator.w3.org/) and [W3C CSS Validator](https://jigsaw.w3.org/css-validator/).  
- **Python** code conforms to **PEP8** (checked with `flake8`/`black`) and includes compound statements (`if`/`loops`).  
- No broken links, no debug mode in production, secrets are in environment variables.

---

## Deployment

1. **Heroku Setup**  
   ```bash
   heroku login
   heroku create your-holiday-club
