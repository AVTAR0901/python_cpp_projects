# Instagram Clone Project

This project was developed as a more complex full-stack application using FastAPI. The goal was to implement several key features commonly found in modern social media applications.

## Technology Stack:
- Backend: FastAPI for API development and authentication.
- Database: SQL database for user, post, and comment management.
- Frontend: ReactJS for building the user interface.

##Features:
- User Authentication: Users can sign up, log in, and log out securely.
- Post Upload: Authenticated users can upload posts, which consist of a photo and caption.
- Post Deletion: Only the user who uploaded a post can delete it.
- Feed: Users can view all posts on their feed.
- Real-time Comments: A comment section is implemented that updates comments in real time without requiring a full page refresh.
- Post Structure: Posts display a photo, caption, comments, the username, and profile picture of the user who uploaded the post, along with a delete button.
- Sticky Header and Footer: A sticky header and footer are implemented for easier navigation.
- Header: Shows "Login" and "Sign Up" buttons when the user is not logged in, or a "Logout" button when logged in.
- Footer: Contains a post upload form for authenticated users.
- APIs with Authorization: Certain API routes require user authentication for accessing or performing actions.
