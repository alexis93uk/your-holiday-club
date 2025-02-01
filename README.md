# Holiday Club

**Author**: Aleksandar Husagic 

## Project Description

Holiday Club is a simple Flask-based web application where users can share their holiday travel stories. Users can:

- View all holiday stories.
- Read each story in detail.
- Add a new holiday story.
- Edit an existing story.
- Delete a story.

The purpose is to create a collaborative environment for travelers to share tips, destinations, and experiences, helping one another plan future trips.

# Table of Contents
1. User Stories
2. Features
3. Technologies
4. Database Structure
5. Manual Testing
6. Code Validation
7. Deployment

## User Stories
Below are some user stories that guided the design and functionality of the application:

1. Visitor: site visitor, can see a list of travel stories so they can discover new travel destinations. 
2. Contributor: User who wants to share travel story.
3. Returning User: The user who previously posted a story, HAS the option to edit the story when mistakesare  found, or just add extra information. 
4. Account Owner: The owner of the story can delete the story. 
5. Inquirer: If someone has any questions, they can contact administrators.

## Features
### 1. CRUD Operations
Create: Add a story via the “Add Story” page.
Read: View all stories in a list (viewstory.html) and detailed single pages (story.html).
Update: Edit any existing story (editstory.html).
Delete: Remove a story from the database (deletestory.html).

### 2.Responsive Design
A simple responsive layout ensures content is accessible on mobile and desktop devices.

### 3.Flash Messages
The app provides immediate feedback (success/error) to users after each action.

### 4.Sample Data
The application seeds a few sample travel stories on first run.

### 5.Contact Form
A basic contact form allows users to submit inquiries.

## Technologies

- **Python** (Flask)
- **SQLite** (Database)
- **HTML5 / CSS3/js**
- **Deployed on**: (Heroku)

## Database Structure
This app uses a single stories table in holiday_club.db:
![image](https://github.com/user-attachments/assets/4cff4d25-4e28-4f4b-a1e1-040871617e43)

## Manual Testing
Below are some manual test procedures to verify the app’s functionality

1. Home Page Test
- Step: I navigated to / (index page).
- Result: I saw a welcome message “Welcome to Holiday Club” and navigation links.

2. View Stories
- Step: I Clicked “View Stories” link from navbar.
- Result: A list of existing sample stories (5 seeded ones) is displayed. Each item shows the location and a preview of the story text.

3. Add New Story
- Step: click “Add Story” link, fill out the location and story_text, submit.
- Result: A success flash message “Story added successfully!” appears, and the user is redirected to “View Stories.” The new story should now appear in the list.

4. View Single Story
- Step: From “View Stories,” click “Read More” on any listed story.
- Result: A detail page (story.html) appears showing the story’s title (location) and the entire text, plus placeholder images.

5. Edit Existing Story
- Step: While on the detail page or the view list, click “Edit.” Change the location or text, submit.
- Result: A success flash message “Story updated successfully!” and the updated details appear on “View Stories.”

6. Delete a Story
- Step: Click “Delete” on a story. Confirm.
- Result: The story is removed from the database, and a success message “Story deleted successfully!” is shown. The story no longer appears in “View Stories.”

7. Contact Form
- Step: Go to “Contact,” fill in Name, Email, and Message, and submit.
- Result: A flash message “Thank you for your message. We’ll get back to you soon!” appears.

8. Error Handling
- Step: Try adding a story without a location or text.
- Result: Flash message “Please provide both location and story text.”

9. Responsiveness
- Step: Resize the browser window or use mobile view in DevTools.
-Result: Navbar collapses or stacks, images scale properly, layout remains usable.

### By performing these manual checks, I confirm that each feature works as intended from the user’s perspective.

# Code Validation

## CSS Validation
![image](https://github.com/user-attachments/assets/a89d0100-e42e-4200-b106-3e409e71521e)



