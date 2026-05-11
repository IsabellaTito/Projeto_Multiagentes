from shared.storage import get_db
from shared.repository import SessionRepository

def init_session(session_id:int = 1):
    db = get_db()
    session_repository = SessionRepository(db)
    session_user = session_repository.get_session_by_id(session_id)

    if session_user is None:
        chat_session = session_repository.create_session()
        session_user = chat_session.id
    
    return session_user

