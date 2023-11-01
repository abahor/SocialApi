# SocialApi
A small social media app built using Fastapi and Postgres

for database initialization:
change the password in the models file then execute these commands:
# alembic init alembic
# alembic revision --autogenerate -m "First revision"
# alembic upgrade head
# alembic downgrade -1
