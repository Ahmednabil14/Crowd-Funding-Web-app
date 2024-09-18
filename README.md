# Crowdfunding Web App

A Django-based web application for launching and managing fundraising campaigns. The platform allows users to create, view, and donate to crowdfunding projects while maintaining a secure and engaging environment for both project creators and backers.

## Features

### 1. Authentication System
- **User Registration**: Users can register by providing first name, last name, email, password, mobile phone (validated for Egyptian phone numbers), and profile picture.
- **Email Activation**: A user must activate their account via an activation email link that expires after 24 hours.
- **Login**: Users can log in using their email and password.
- **User Profile**: Users can view and edit their profile, including viewing their projects and donations.
- **Account Deletion**: Users can delete their account with confirmation and password re-entry for security.

### 2. Project Management
- **Create a Project**: Users can create a fundraising campaign with:
  - Title, details, and multiple images.
  - Category (predefined by admins).
  - Target amount (in EGP).
  - Tags, start, and end time.
- **Project Interaction**:
  - Users can view and donate to any project.
  - Add comments to projects.
  - Report inappropriate projects.
  - Rate projects.
  - Project creators can cancel a project if donations are less than 25% of the target.
- **Project Display**:
  - A project’s average rating is shown.
  - Images are displayed in a slider.
  - Related projects are displayed based on tags.

### 3. Homepage
- **Latest Projects**: Displays the five most recent projects.
- **Search**: Users can search projects by title or tags.

## Tech Stack

- **Framework**: Django
- **Database**: SQLite (default), but can be changed to PostgreSQL, MySQL, or others.
- **Frontend**: HTML, CSS, JavaScript (can integrate with Bootstrap for styling).