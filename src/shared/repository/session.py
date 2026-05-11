from shared.models import ChatSession
from shared.storage.database import Database

class SessionRepository:
    def __init__(self, db: Database):
        self.db = db

    def create_session(self) -> ChatSession:
        with self.db.session_scope() as session:
            chat = ChatSession()
            session.add(chat)
            session.flush()  # pega o ID antes do commit
            return chat
        
    def get_session_by_id(self, session_id: int) -> int | None:
        with self.db.session_scope() as session:
            chat = session.get(ChatSession, session_id)
            return chat.id if chat else None
        
    def get_all_sessions(self):
        with self.db.session_scope() as session:
            return (
                session.query(ChatSession)
                .order_by(ChatSession.created_at.desc())  # mais recentes primeiro
                .all()
            )