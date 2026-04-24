from shared.models import ChatSession, Message
from shared.storage.database import Database

class ChatRepository:
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

    def create_message(self, session_id: int, role: str, content: str) -> Message:
        with self.db.session_scope() as session:
            msg = Message(
                session_id=session_id,
                role=role,
                content=content
            )
            session.add(msg)
            session.flush()
            return msg

    def get_messages(self, session_id: int):
        with self.db.session_scope() as session:
            return (
                session.query(Message)
                .filter(Message.session_id == session_id)
                .order_by(Message.created_at)
                .all()
            )
        
    def get_messages_as_dict(self, session_id: int):
        with self.db.session_scope() as session:
            messages = (
                session.query(Message)
                .where(Message.session_id == session_id)
                .order_by(Message.created_at)
                .all()
            )

            return [
                {"role": m.role, "content": m.content}
                for m in messages
            ]