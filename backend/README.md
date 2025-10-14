## Structure

- `/scripts` : mainly stuff to test and populate fake data
- **app**: where most loigic leaves
  - **api**: routes and depenedcies
  - **core**: configuration (env variables) and seucrity (hashing, jwt, verifying, refreshing)
  - **models**: data models that serve both as models for _ORM_ and as general schema.
    - client.py
    - user.py
    - meeting.py
    - token.py (will probably be deleted)
  - **services**:
    - user_service.py: logic to handle logic and logout
    - #TODO: serivce for crud operations and querying operations for users
  - **database.py**: db connection and inittializing (runs on startup)
  - **main.py**: main app file, import routes, init db, start service, cross service
- **main.py**: for lazies- activate env and run `uvicorn app.main:app --reload`

### TODOS

**init**

- [x] user schema
- [x] meeting schema
- [x] client schema
- [x] db connection and init
      **API**
- [x] login api
- [ ] user crud client api
- [ ] user crud meeting api
- [ ] user get all data api
      **Advanced**
- [ ] make advanced queries per user
- [ ] get numpy matrices for frontend to show graphs
