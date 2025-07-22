# 🛠️ Product Management API

This project provides a RESTful API for managing products, categories, and user accounts. It is designed to support both regular users and admin users with different levels of access.

---

## 📌 Base URL

http://<your-domain-or-localhost>/api


---

## 📂 API Endpoints

### 📦 Product Endpoints

| Endpoint               | Method | Path                | Description                                | Access |
|------------------------|--------|---------------------|--------------------------------------------|--------|
| Product List           | GET    | `/products/`        | Get a list of all products                 | User   |
| Create Product         | POST   | `/products/`        | Create a new product                       | Admin  |
| Retrieve Product by ID | GET    | `/products/{id}/`   | Get details of a specific product by ID    | User   |
| Update Product by ID   | PUT    | `/products/{id}/`   | Update details of a specific product by ID | Admin  |
| Delete Product by ID   | DELETE | `/products/{id}/`   | Delete a specific product by ID            | Admin  |

---

### 🗂️ Category Endpoints

| Endpoint                 | Method | Path                  | Description                                   | Access |
|--------------------------|--------|-----------------------|-----------------------------------------------|--------|
| Category List            | GET    | `/categories/`        | Get a list of all categories                  | User   |
| Create Category          | POST   | `/categories/`        | Create a new category                         | Admin  |
| Retrieve Category by ID  | GET    | `/categories/{id}/`   | Get details of a specific category by ID      | User   |
| Update Category by ID    | PUT    | `/categories/{id}/`   | Update details of a specific category by ID   | Admin  |
| Delete Category by ID    | DELETE | `/categories/{id}/`   | Delete a specific category by ID              | Admin  |

---

### 👤 User Management Endpoints

| Endpoint                     | Method | Path                      | Description                                         | Access |
|------------------------------|--------|---------------------------|-----------------------------------------------------|--------|
| User List                    | GET    | `/users/`                 | Get a list of all users (admin-only)               | Admin  |
| Get User By ID               | GET    | `/users/{user_id}/`       | Get details of a specific user by ID (admin-only)  | Admin  |
| Create User                  | POST   | `/users/`                 | Create a new user (admin-only)                     | Admin  |
| Update User By ID            | PUT    | `/users/{user_id}/`       | Update details of a specific user by ID (admin-only) | Admin |
| Delete User By ID            | DELETE | `/users/{user_id}/`       | Delete a specific user by ID (admin-only)          | Admin  |
| Get My Account Info          | GET    | `/account/`               | Get information about the authenticated user       | User   |
| Edit My Account Info         | PUT    | `/account/`               | Edit the information of the authenticated user     | User   |
| Remove My Account            | DELETE | `/account/`               | Remove the account of the authenticated user       | User   |

---

### 🔐 Authentication Endpoints

| Endpoint             | Method | Path                 | Description                                           | Access |
|----------------------|--------|----------------------|-------------------------------------------------------|--------|
| User Signup          | POST   | `/auth/signup/`      | Register a new user                                  | User   |
| User Login           | POST   | `/auth/login/`       | Authenticate and generate access tokens              | User   |
| Refresh Access Token | POST   | `/auth/refresh/`     | Refresh an access token using a refresh token        | User   |

---

### 📚 API Documentation

| Endpoint       | Path             | Description                                 | Access |
|----------------|------------------|---------------------------------------------|--------|
| Swagger UI     | `/docs/`         | Swagger UI for API documentation            | User   |
| Swagger JSON   | `/openapi.json`  | OpenAPI JSON for API documentation          | User   |
| ReDoc UI       | `/redoc/`        | ReDoc UI for API documentation              | User   |

---

## 🔒 User Roles

- **User**: Can browse and manage their own account, view product and category information.
- **Admin**: Has full control including management of users, products, and categories.

---

## 🚀 Getting Started

1. Clone the repository:

   ```bash
   git clone <repository-url>
    ```
2. Install dependencies and set up environment.

3. Run the development server:
    ```
    uvicorn main:app --reload
    ```

📌 You can update the base URL, authentication mechanism, or documentation tools depending on your actual setup.