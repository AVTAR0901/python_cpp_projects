# Warehouse & Store Project using Microservices

This project was developed as a full-stack application to explore microservice architecture, Redis (NoSQL) database integration, and asynchronous functionality for real-time operations.

## Technology Stack:
- Backend: FastAPI for building microservices and handling API communication.
- Database: Redis (NoSQL) for managing data, asynchronous tasks, and real-time updates.
- Frontend: ReactJS for creating an interactive and dynamic user interface.

## Features:
- Microservice Architecture: Implemented to enable communication between the Warehouse and Store services through API calls.
- Asynchronous Tasks with Redis Streams: Background tasks such as order processing and real-time errors were handled asynchronously using Redis streams, ensuring efficient and scalable performance.
- Product Management:
             -- Users in the Warehouse service can create new products and delete existing ones.
             -- Products have a unique product ID, name, quantity, and price.
- Ordering System:
             -- Users in the Store service can place orders for products in specified quantities.
             -- The available quantity of products in the Warehouse is updated in real-time as orders are placed from the Store, ensuring accurate stock management.
             -- On the ordering page, the price dynamically updates based on the quantity selected by the user.
- Order Notifications: After placing an order, the user is notified of the quantity ordered and confirmed.
