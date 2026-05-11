from shared.models import Message
from shared.storage.database import Database

class MessageRepository:
    def __init__(self, db: Database):
        self.db = db

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