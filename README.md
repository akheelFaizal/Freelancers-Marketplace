# Freelancers Platform API

A RESTful API built with Django REST Framework for a freelancing platform where clients can post projects and freelancers can bid, get hired, and complete contracts.

## 🔧 Features

- User registration with roles (client/freelancer)
- JWT-based authentication
- Profile management (view/update/complete)
- Skill management
- Project creation, update, and listing (open/closed)
- Bidding system per project/freelancer
- Contract management and project completion


---

## Authentication
- JWT Token-based Authentication is required for most routes.
- Use `/api/token/` and `/api/token/refresh/` for obtaining and refreshing tokens.

---

## Endpoints

### User Management

#### Create User

**Request Body:**
```json

POST /create/user/
**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "is_client": true/false,
  "is_freelancer": true/false
}
Response:
201 Created / 400 Bad Request

View All Users
GET /view/users/
Returns a list of all users.

Filtered User Details (by role)
GET /view/user-details/?user_type=client|freelancer
Requires authentication.

Authenticated User Profile
GET /profile/me/
Returns the logged-in user's details.

Update Authenticated User
PUT /profile/update/
Request Body:
{
  "username": "string",
  "email": "string",
  "is_client": true/false,
  "is_freelancer": true/false
}
Profile Management
Complete/Update Profile

POST /profile/complete/
Requires authentication.
Request Body:
Partial profile data (see UserProfileSerializer).

Skills
Add Skill
POST /add/skills/
Request Body:
{
  "skill": "string"
}

Freelancer Listings
List Freelancers (optional filter by skill)
GET /list/freelancers/?skill=Python
Returns freelancers with or without skill filter.

Project Management
Create Project
POST /project/
Request Body: Project fields (see ProjectSerializer).

View All Projects
GET /project/
Returns all projects.

Update Project
PUT /project/?pid=<project_id>
Request Body: Partial fields to update.

List Open Projects
GET /open/project/

List Closed Projects
GET /closed/project/

Bids
Place a Bid
POST /bid/
Requires authentication.
Request Body: Bid fields (see BidSerializer).

View Bids for Client Projects
GET /bid/
Requires authentication. Lists all bids placed on projects of the logged-in client.

View Bids for a Project
GET /bid/<project_id>
View Bids by a Freelancer
GET /bid/<freelancer_id>

Contracts
Close Project and Create Contract
POST /bid/close/
Request Body: Contract data (see ContractSerializer).

Mark Contract/Project as Completed
PUT /contract/completed/<project_id>
Marks the contract as completed and sets the end_date.

Status Codes :

200 OK

201 Created

400 Bad Request

401 Unauthorized

404 Not Found

500 Internal Server Error



