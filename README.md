# Digital Art Marketplace

An online platform for buying and posting digital art pieces.

## Application Suitability

### Idea relevancy

Digital Art Station addresses the growing demand for platforms that enable digital artists to sell and showcase their work. With the rise of **digital art ownership**, it meets a current market need by connecting artists and buyers.

### Using microservices
* Provide scalability, modularity
* Independent management

### Real-world examples
* Etsy
* DeviantArt

These platforms use microservices to manage user accounts, transactions, and content independently, offering scalability and fault tolerance while serving similar needs.

## Service Boundaries
Each microservice will be responsible for a specific aspect of the platform:

* Login/Authorization Service: Handles user authentication, session management, and JWT-based authorization.
* Artwork Management Service: Manages artwork uploads, categorization and pricing. Handles digital storage and metadata for each piece of art.

### System Architecture

![System diagram](/img/PAD_Diagram.drawio.png "System diagram")

## Technology Stack and Communication Patterns
* **Flask** for developing the RESTful API microservices.
* **NodeJS** for developing the API gateway, managing routing and communication between client requests and backend services.
* **Docker** for containerizing services, ensuring scalability, isolation, and easy deployment.
* **PostgreSQL** for transactional data (user accounts, artwork data), and **Redis** for cache management.
* **JWT** for secure login and authorization.
* **gRPC** for efficient, low-latency communication between services.
* **HTTP/REST** for client-facing APIs.

## Data Management

* User data will be stored in **PostgreSQL**. Thus handling user profiles, login credentials (hashed), and artwork favoriting.
* **Redis** will be used for the caching of popular artworks and recommendations to optimize performance.

## Deployment and Scaling

* Services will be deployed using **Docker** containers, ensuring isolation for each service and allowing for independent scaling.
* Login/Authorization service will be prioritized for **vertical scaling** to handle increasing user traffic. 
* Artwork Management will be scaled based on storage needs and the volume of artwork uploads.