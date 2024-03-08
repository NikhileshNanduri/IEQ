# Interactive EQ Assessment

Flask-based application for ecommerce backend. It provides various endpoints for managing users, products, and authentication.

## Endpoints

1. **Home**: `GET /` - Retrieves the home page of the application.
2. **Authentication**:
   - **Auth**: `POST /auth` - Authenticates users and generates access tokens.
   - **Register**: `POST /register` - Registers new users.
3. **Products**:
   - **Get All Products**: `GET /products` - Retrieves all products.
   - **Get Specific Product**: `GET /products/<product_id>` - Retrieves a specific product.
   - **Add Product**: `POST /products` - Adds a new product.
   - **Update Product**: `PUT /products/<product_id>` - Updates an existing product.
   - **Delete Product**: `DELETE /products/<product_id>` - Deletes a product.
4. **Users**:
   - **Get All Users**: `GET /users` - Retrieves all users.
   - **Get Specific User**: `GET /users/<username>` - Retrieves a specific user.
   - **Delete User**: `DELETE /users/<username>` - Deletes a user.

## Usage

1. **Setup**:
   - Clone the repository.
   - Install Docker and Docker Compose if not already installed.
2. **Running the Application**:
   - Execute `docker-compose up` command in the project directory.
   - The following containers will spin up-
        - **flask_app**: Flask application container serving the backend API.
        - **mongo_db**: MongoDB container serving as the primary database.
        - **redis**: Redis container used for caching.   
   - The application will be available at `http://localhost:4000`.
3. **Testing Endpoints**:
   - Import the provided Postman collection.
   - Set up environment variables for `TOKEN_ADMIN` and `TOKEN_USER` with valid JWT tokens.
   - Run the requests to interact with the API endpoints.


## Testing

- The application can be tested by importing the provided Postman collection (Postman Endpoints.json)

## Implementation

- The application is built using Python with Flask framework for the backend.
- MongoDB is used as the primary database for storing user and product information.
- Redis is used for caching to improve application performance.
- JWT (JSON Web Tokens) are utilized for user authentication and authorization.
- Endpoints are organized using Flask Blueprints for modularity and scalability.
- Docker Compose is used for containerization and managing application dependencies.
- Nginx has been setup to allow load balancing and weighted load balancing between multiple instances of flask_app hosted


## Enhancements
- Can enhance error handling and logging for improved debugging.
- Can setup instrumentation for monitoring application performance and errors
- Need unit-tests and integration tests
- Database high availability features need to be added


