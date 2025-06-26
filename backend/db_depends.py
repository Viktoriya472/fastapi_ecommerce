from app.backend.db import SessoinLocal


async def get_db():
    db = SessoinLocal()
    try:
        yield db
    finally:
        db.close()
