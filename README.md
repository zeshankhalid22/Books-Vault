
# Books-Vault - Book Collection and Sharing Platform

Books-Vault is a web application that allows users to browse books, submit their own book additions (pending admin approval), and manage their reading collections. The application is built with a Python FastAPI backend and React TypeScript frontend.

## Features

- **Book Browsing**: View all available books with pagination
- **Book Search**: Find books by title, author, or other criteria
- **User Authentication**: Secure login and registration functionality
- **Book Upload Requests**: Users can submit books to be added to the library
- **Admin Approval System**: Administrators can review and approve user book submissions
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
Library App/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   └── routers/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── static/
│   └── main.py
└── frontend/
    ├── app/
    │   ├── api/
    │   ├── components/
    │   ├── hooks/
    │   ├── routes/
    │   ├── store/
    │   ├── types/
    │   └── utils/
    ├── public/
    └── package.json
```

## Tech Stack

### Backend
- Python 3.9+
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- JWT Authentication

### Frontend
- React 18
- TypeScript
- Zustand (State Management)
- Axios (API client)
- TailwindCSS
- React Router v7

## Getting Started

### Prerequisites
- Node.js 16+
- Python 3.9+
- PostgreSQL

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd "Library App/backend"
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and settings
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd "Library App/frontend"
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:3000`

## API Endpoints

### Public Endpoints
- `GET /books/`: Get all books (paginated)
- `GET /books/{id}`: Get book by ID
- `GET /books/search/?q=query`: Search for books

### Authentication Endpoints
- `POST /login`: User login
- `POST /refresh`: Refresh access token
- `GET /users/me/`: Get current user details

### User Endpoints
- `POST /users/`: Create new user
- `GET /upload_request/my`: Get current user's upload requests
- `POST /upload_request/`: Create new upload request

### Admin Endpoints
- `GET /admin/users`: Get all users
- `GET /admin/upload_request/{id}`: Get specific upload request
- `POST /admin/books/`: Add a new book
- `DELETE /admin/books/{id}`: Delete a book


## TODO

- **Fix Book Store Data Handling**: The `fetchBooks` function in `bookStore.ts` has a typo (`dataa` vs `data`) that needs correction
- **Implement Contact Form Submission**: The contact form in `contact.tsx` needs backend API integration
- **Complete Logout Functionality**: The backend logout endpoint is currently a placeholder
- **Implement Book Upload Interface**: Create UI for the book upload request feature
- **Add Admin Panel**: Develop the admin interface for managing book upload requests
- **Fix Token Refresh Mechanism**: The token refresh mechanism needs to be properly tested
- **Add Form Validation**: Implement proper validation for all forms including login and contact
- **Create User Profile Page**: Allow users to view and edit their profile information
- **Implement Pagination Controls**: Add UI components for navigating through paginated book results
- **Add Book Details Page**: Create a dedicated page for viewing comprehensive book information
- **Create User Registration Flow**: Implement the sign-up process for new users
- **Add Error Handling Components**: Develop consistent error display across the application

This section highlights the pending frontend tasks that need attention while maintaining the existing functionality of your Books-Vault application.

## Contact

For questions or feedback about BookShelf, email me at `zeshanofbhakkar@gmail.com`