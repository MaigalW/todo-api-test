# todo-api

API REST for task managing

## Test users

| User    | Password   | Role  |
|---------|------------|-------|
| admin   | admin      | admin |
| user1   | user       | user  |
| user2   | user       | user  |

---

### Implemented cruds
- Create, read, update and delete task.
- Task structure:
  - 'id': Generated using MongoDB's ObjectId.
  - 'title': Title (mandatory).
  - 'description': Small descriptory text (optional).
  - 'status': '"pending"', '"in progress"' or '"completed"'.
  - 'created_at', 'updated_at': automatically generated and updated.
- Added filters for tasks by:
  - 'status'
  - 'created_at' date range

### Authentication
- Using JWT.
- Actions accesible only by logging in.
- Roles:
  - 'admin': Full access. Can also manage users.
  - 'user': Can only manage own tasks.


## Pytests
Tests using 'pytest' y 'pytest-asyncio'.

'''bash
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
'''

## Docker
- Use .env.example for creating your own .ev
- Run:
   - docker compose up --build

## AWS

-READ DEPLOY.md
