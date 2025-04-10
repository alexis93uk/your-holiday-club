# Holiday Club
https://your-holiday-club-d5454424f4de.herokuapp.com/
**Author**: Aleksandar Husagic  

Holiday Club is a simple Flask-based web application where users can share their holiday travel stories. The purpose is to create a collaborative environment for travelers to exchange tips, destinations, and experiences, helping each other plan their future trips.

---

## Table of Contents
1. [Project Description](#project-description)  
2. [User Stories](#user-stories)  
3. [Features](#features)  
4. [Technologies](#technologies)  
5. [Database Structure](#database-structure)  
6. [Manual Testing](#manual-testing)  
7. [Code Validation](#code-validation)  
8. [Deployment](#deployment)  
9. [Installation & Usage (Local)](#installation--usage-local)  
10. [License](#license)

---

## Project Description

Holiday Club is a straightforward Flask-based web application where users can:

- View all holiday stories.  
- Read each story in detail.  
- Add a new holiday story.  
- Edit an existing story.  
- Delete a story.  

It fosters a **community-driven** space for sharing travel experiences and advice.

---

## User Stories

Below are some user stories that guided the design and functionality of the application:

1. **Visitor**: As a site visitor, I want to see a list of travel stories so I can discover new travel destinations.  
2. **Contributor**: As a user who wants to share a travel story, I need a simple way to add my story so that others can read it.  
3. **Returning User**: As a user who previously posted a story, I want an option to edit the story if I find mistakes or wish to add more information.  
4. **Account Owner**: As the owner of a story, I want the ability to delete it if I no longer want it published.  
5. **Inquirer**: As someone with questions, I want a contact form to reach administrators.

---

## Features

1. **CRUD Operations**  
   - **Create**: Add a story via the “Add Story” page.  
   - **Read**: View all stories in a list (`viewstory.html`) and detailed single pages (`story.html`).  
   - **Update**: Edit any existing story (`editstory.html`).  
   - **Delete**: Remove a story from the database (`deletestory.html`).

2. **Responsive Design**  
   - A simple responsive layout ensures content is accessible on mobile and desktop devices.

3. **Flash Messages**  
   - The app provides immediate feedback (success/error) to users after each action.

4. **Sample Data**  
   - The application seeds a few sample travel stories upon first run.

5. **Contact Form**  
   - A basic contact form allows users to submit inquiries.

---

## Technologies

- **Python** (Flask)  
- **SQLite** (Database)  
- **HTML5 / CSS3 / minimal JS**  
- **Deployment**: Heroku (or any similar hosting)

---

## Database Structure

This app uses a single `stories` table in **`holiday_club.db`**. The simplified schema is as follows:

| Column     | Type         | Description                               |
|------------|--------------|-------------------------------------------|
| `id`       | Integer (PK) | Auto-increment primary key                |
| `location` | Text         | Name of the travel destination            |
| `story_text` | Text       | Detailed story or experience              |

A quick visual representation:

stories ┌─────────────┐ │ id (PK) │ │ location │ │ story_text │ └─────────────┘


*(Screenshot or diagram reference, if desired.)*

---

## Manual Testing

Below are some manual test procedures to verify the app’s functionality:

1. **Home Page Test**  
   - **Step**: Navigate to `/` (index page).  
   - **Result**: Displays a welcome message “Welcome to Holiday Club” and navigation links.

2. **View Stories**  
   - **Step**: Click “View Stories” link from navbar.  
   - **Result**: A list of existing sample stories (5 seeded) is displayed. Each item shows the location and a preview of the story text.

3. **Add New Story**  
   - **Step**: Click “Add Story” link, fill out the location and story text, then submit.  
   - **Result**: Displays a success flash message “Story added successfully!” and redirects to “View Stories.” The new story appears in the list.

4. **View Single Story**  
   - **Step**: From “View Stories,” click “Read More” on any listed story.  
   - **Result**: A detail page (`story.html`) shows the story’s title (location) and the entire text, plus placeholder images.

5. **Edit Existing Story**  
   - **Step**: While on the detail page or the view list, click “Edit.” Change the location or text, then submit.  
   - **Result**: Success flash message “Story updated successfully!” and the updated details appear on “View Stories.”

6. **Delete a Story**  
   - **Step**: Click “Delete” on a story. Confirm the deletion.  
   - **Result**: The story is removed from the database, and a success message “Story deleted successfully!” is shown. The story no longer appears in “View Stories.”

7. **Contact Form**  
   - **Step**: Go to “Contact,” fill in Name, Email, and Message, then submit.  
   - **Result**: Displays a flash message “Thank you for your message. We’ll get back to you soon!”

8. **Error Handling**  
   - **Step**: Try adding a story without a location or text.  
   - **Result**: Displays a flash message “Please provide both location and story text.”

9. **Responsiveness**  
   - **Step**: Resize the browser window or use mobile view in DevTools.  
   - **Result**: Navbar collapses or stacks, images scale properly, and the layout remains usable.

By performing these checks, we confirm that each feature works as intended from the user’s perspective.

---

## Code Validation

### HTML & CSS Validation
- **HTML**: Validated using [W3C Markup Validation](https://validator.w3.org/).  
- **CSS**: Validated using [W3C CSS Validator](https://jigsaw.w3.org/css-validator/). 

*(Include screenshots or mention results as appropriate.)*

### Python (PEP8)
- Ensured Python code is **PEP8**-compliant (indentation, variable naming) using a linter such as **Flake8** or **Black**.

---

## Deployment

Below is how the project was deployed to **Heroku**:

1. **Heroku Setup**  
   - Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).  
   - Log in via `heroku login`.

2. **Create the Heroku App**  
   ```bash
   heroku create holiday-club-app

3. **Procfile & Requirements**
   - Include a Procfile with web: gunicorn app:app
   - Ensure requirements.txt has Flask, gunicorn, etc.

4. **Set Environment Variables**
   heroku config:set SECRET_KEY="your_secret_key"
   heroku config:set DEBUG_MODE="False"

5. **Push to Heroku**
   git push heroku main

6. **Open the App**
    heroku open
   https://your-holiday-club-d5454424f4de.herokuapp.com/ 
7. **Troubleshooting**
    Use heroku logs --tail to check logs if something goes wrong.

