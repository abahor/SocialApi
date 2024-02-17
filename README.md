# SocialApi
A small social media app built using Fastapi and Postgres

for database initialization:
change the password in the models file then execute these commands:
- alembic init alembic
- alembic revision --autogenerate -m "First revision"
- alembic upgrade head

### Note: ----- after executing this command go to alembic.ini and change the sqlalchemy url and the metatarget in the env.py file

for downgrading database
- alembic downgrade -1
