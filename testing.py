# import psycopg
#
# try:
#     with psycopg.connect("dbname=fastapi user=postgres password=hpprobook450g3*") as conn:
#         with conn.cursor() as cur:
#             # Execute a command: this creates a new table
#
#             cur.execute("SELECT * FROM posts")
#             cur.fetchone()
#
#             for record in cur:
#                 print(record)
#             conn.commit()
# except Exception as e:
#     print(e)

import os
print(os.getcwd())