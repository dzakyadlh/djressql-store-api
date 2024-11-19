# Django Store API with Redis Caching

Django-based API for managing products and categories in a store. The API use Redis for caching frequently accessed data to optimize database queries.

### Tech Stack

1. **Django** for API development.
2. **SQLite** as the database for simplicity.
3. **Redis** as a caching layer, to store frequently accessed data temporarily.
4. **django-redis** for connecting Django with Redis.

### Models

1. **Category**
    - Fields:
        - `name`: String, max length 255, unique.
        - `description`: Text, optional.
2. **Product**
    - Fields:
        - `name`: String, max length 255.
        - `description`: Text, optional.
        - `price`: Decimal, max 10 digits with 2 decimal places.
        - `category`: ForeignKey, links to a `Category`.
        - `created_at`: Date and time when the product was created.
        - `updated_at`: Date and time when the product was last updated.

### Endpoints

1. **Category Endpoints**
    - **GET /api/categories/**: List all categories.
    - **POST /api/categories/**: Create a new category.
    - **GET /api/categories/{id}/**: Retrieve a category by ID.
    - **PUT /api/categories/{id}/**: Update a category.
    - **DELETE /api/categories/{id}/**: Delete a category.
2. **Product Endpoints**
    - **GET /api/products/**: List all products with optional filtering.
        - Optional Filters:
            - `category`: Filter by category name.
            - `price_min` and `price_max`: Filter within a price range.
    - **POST /api/products/**: Create a new product.
    - **GET /api/products/{id}/**: Retrieve a product by ID.
    - **PUT /api/products/{id}/**: Update a product.
    - **DELETE /api/products/{id}/**: Delete a product.

### Caching with Redis

1. **Cache Keys**
    - Categories: `store:categories`
    - Products: `store:products`
2. **Redis Configuration**:
Configured Redis in Django settings with a 5-minute cache timeout.
3. **Caching Strategy**:
    - **GET Requests**: Retrieve data from Redis if cached; otherwise, fetch from the database and store it in Redis.
    - **POST, PUT, DELETE Requests**: Invalidate the cache to ensure consistency.

### Instructions

1. **Install Required Packages**:
   Install all the requirements in the requirements.txt using this command line
   ```bash
   pip install -r requirements.txt
   ```
2. **Install Redis**:
   Go to Redis website and install Redis if you haven't already
    [Redis Download](https://redis.io/downloads/)
3. **Migrate the Database**:
   Run migrations
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4. **Start Redis Server**:
   Open a terminal and run this command to start redis server
    ```bash
    redis-server
    ```
5. **Start Django Server**:
   Start Django server by running this line on your IDE terminal
    ```bash
    python manage.py runserver
    ```
6. **Test the API**:
   Feel free the test the API if you want
    ```bash
    python manage.py test
    ```
