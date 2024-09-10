# Digital Art Marketplace

An online platform for buying and posting digital art pieces.
    

## Application Suitability

### Idea relevancy

Digital Art Station addresses the **growing demand** for platforms that enable digital artists to sell and showcase their work. With the rise of **digital art ownership**, it meets a current market need by connecting artists and buyers together.

### Using microservices

* Provide scalability, modularity.
* Independent management.

### Real-world examples
- Etsy:

    - **Microservices** for user accounts, transactions, and product listings.
    - Search, notifications, and messaging handled independently.
    - **Integration** with third-party payment and shipping services.

- DeviantArt:

    - **Independent services** for user profiles, artwork uploads, and transactions.
    - Search, notifications, and community features (likes, comments, groups) **managed separately**.

## Service Boundaries
* **Login service** will handle user authentication, session management, and JWT-based authorization.
* **Artwork Management** service will administer artwork uploads, categorization and pricing.

### System Architecture

![System diagram](/img/PAD_Diagram.drawio.png "System diagram")

## Communication Patterns

### Synchronous

* **gRPC** for efficient, low-latency communication between services.
* **HTTP/REST**  for client-facing APIs, REST operates over HTTP with a synchronous request-response approach.

### Asynchronous 

* **WebSockets** for real-time, full-duplex communication for events like notifications.


## Technology Stack
* **Flask** for developing the RESTful API microservices.
* **ExpressJS** for developing the API gateway, managing routing and communication between client requests and backend services.
* **Swagger/Postman** for designing, testing, and documenting APIs.
* **Docker** for containerizing services, ensuring scalability, isolation, and easy deployment.
* **PostgreSQL** for transactional data (user accounts, artwork data). 
* **Redis** for cache management.
* **JWT** for secure login and authorization.

## Data Management
* User data will be stored in **PostgreSQL**, handling user profiles, hashed login credentials, and artwork favorites.
* **Redis** will be used to cache popular artworks and recommendations, optimizing performance.

## Data between Services

### Database models

* **User**
```json
    {
        "id": "int",
        "username": "string", 
        "email": "string",
        "password": "string",
    }
```

* **ArtPiece**
```json
    {
        "id": "int",
        "title": "string", 
        "description": "string"
        "price": "float"
        "category": "string"
        "image_url": "string"
        "created_at": "dateTime"
    }
```

### Login Endpoints
#### /api/auth/login

**Method**: POST

- **Body**

    ```json
    {
    "email": "user@ex.com",
    "password": "securepass"
    }
    ```
- **Response**

    **Status**: 200 OK

    ```json
    {
    "message": "Login successful",
    "token": "JWT"
    }
    ```

    **Status**: 401 Unauthorized
    ```json
    {
    "message": "Invalid email or password"    
    }
    ```

#### /api/auth/register

**Method**: POST

- **Body**

    ```json
    {
    "username": "name",
    "email": "artist@ex.com",
    "password": "pass",
    "confirm_password": "pass"
    }
    ```
- **Response**

    **Status**: 201 Created

    ```json
    {
    "message": "User registered successfully",
    }
    ```

    **Status**: 400 Bad Request
    ```json
    {
    "message": "Passwords do not match"    
    }
    ```

### Artwork Management Endpoints

#### /api/artworks/{id}

**Method**: GET

- **Parameters**
    - `id`: ID of the artwork

- **Response**

    **Status**: 200 Success

    ```json
    {
        "title": "Artwork Title",
        "description": "This is an example.",
        "price": 150.00,
        "category": "Digital Painting",
    }
    ```

    **Status**: 404 Not Found
    ```json
    {
        "message": "Artwork not found"    
    }
    ```

**Method**: PUT

- **Parameters**
    - `id`: ID of the artwork

- **Headers**
    ```json
    {
        "Authorization": "Bearer <JWT_token>"
    }

- **Body**

    ```json
    {
        "title": "Artwork Title",
        "description": "This is an example.",
        "price": 150.00,
        "category": "Digital Painting",
    }
    ```

- **Response**

    **Status**: 200 Success

    ```json
    {
        "message": "Artwork updated successfully"
    }
    ```

    **Status**: 400 Bad Request
    ```json
    {
        "message": "Invalid artwork data"    
    }
    ```

    **Status**: 404 Not Found
    ```json
    {
        "message": "Artwork not found"   
    }
    ```

**Method**: DELETE

- **Parameters**
    - `id`: ID of the artwork

- **Headers**
    ```json
    {
        "Authorization": "Bearer <JWT_token>"
    }
    ```

- **Response**

    **Status**: 200 Success

    ```json
    {
        "message": "Artwork deleted successfully"
    }
    ```

    **Status**: 401 Unauthorized
    ```json
    {
        "message": "Unauthorized: Invalid or missing token"    
    }
    ```

    **Status**: 404 Not Found
    ```json
    {
        "message": "Artwork not found"   
    }
    ```


#### /api/artworks/

**Method**: GET

- **Response**

    **Status**: 200 Success

    ```json
    [
        {
            "title": "Artwork Title 1",
            "description": "This is an example.",
            "price": 150.00,
            "category": "Digital Painting"
        },
        {
            "title": "Artwork Title 2",
            "description": "Another example.",
            "price": 200.00,
            "category": "Photography"
        }
    ]
    ```

    **Status**: 500 Internal Server Error
    ```json
    {
        "message": "Unable to retrieve artworks"     
    }
    ```

**Method**: POST

- **Headers**
    ```json
    {
        "Authorization": "Bearer <JWT_token>"
    }

- **Body**

    ```json
    {
        "title": "Artwork Title",
        "description": "This is an example.",
        "price": 150.00,
        "category": "Digital Painting",
    }
    ```

- **Response**

    **Status**: 201 Created

    ```json
    {
        "message": "Artwork uploaded successfully",
    }
    ```

    **Status**: 400 Bad Request
    ```json
    {
        "message": "Invalid artwork data"    
    }
    ```

#### /api/artworks/popular

**Method**: GET

- **Response**

    **Status**: 200 Successful

    ```json
    [
        {
            "title": "Popular Artwork 1",
            "description": "This is an example."
            "price": 200.00,
            "category": "Illustration"
        },
        {
            "title": "Popular Artwork 2",
            "description": "This is another example."
            "price": 300.00,
            "category": "Digital Painting"
        }
    ]
    ```

    **Status**: 500 Internal Server Error
    ```json
    {
        "message": "Error fetching popular artworks"    
    }
    ```


### Other Endpoints

#### /api/status

**Method**: GET

- **Response**

    **Status**: 200 Successful

    ```json
    {
        "status": "OK",
        "services": {
            "login_service": 
            {
                "status": "Running",
                "response_time": "120ms"
            },
            "artwork_service": 
            {
                "status": "Running",
                "response_time": "150ms"
            }
        }
    }
    ```

    **Status**: 500 Internal Server Error

    ```json
    {
        "status": "Error",
        "message": "One or more services are not responding"
    }
    ```

#### /api/subscribe

**Method**: POST

- **Body**

    ```json
    {
        "user_id": "10",
        "artist_id": "14"
    }
    ```

- **Response**

    **Status**: 200 Successful

    ```json
    {
        "message": "Subscription successful"
    }
    ```


#### /api/notify

**Method**: POST

- **Body**
    ```json
    {
        "artist_id": "14",
        "notification": "New artwork released!"
    }
    ```

- **Response**

    **Status**: 200 Successful

    ```json
    {
        "message": "Notification sent to subscribers",
        "artist_id": "14",
        "notification": "New artwork released!"
    }
    ```

## Deployment and Scaling

* Services will be deployed using **Docker** containers, ensuring isolation for each service and allowing for independent scaling.
* Both services will be **scaled horizontally**  ensuring **better performanc**e and **reliability** by distributing the load across multiple containers, allowing the system to handle more traffic and achieve **higher availability**.
* The deployment process will be made using **Docker Compose**, which will coordinate the **multi-container configuration**. It makes network, volume, and scalability settings for each service simpler.