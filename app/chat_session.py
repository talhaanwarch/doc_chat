from fastapi import HTTPException
# from sqlmodel import Session, delete
from .database import SessionLocal, QueryDB
import shortuuid

class ChatSession:
    """
    Class for loading and saving chat session history to a database.
    """

    @staticmethod
    def load_history(session_id):
        session = SessionLocal()
        results = session.query(QueryDB).filter(QueryDB.session_id == session_id).all()
        session.close()

        result = [
            {'type': 'human', 'data': {'content': row.query, 'additional_kwargs': {}, 'example': False}}
            for row in results
        ] + [
            {'type': 'ai', 'data': {'content': row.answer, 'additional_kwargs': {}, 'example': False}}
            for row in results
        ]

        return result

    @staticmethod
    def save_sess_db(client_email,  session_id, query, answer, cost,
                     query_date,query_time, response_time):
        
        db = QueryDB(query=query, answer=answer, session_id=session_id, 
                     client_email = client_email,
                      client_id=shortuuid.uuid(client_email), 
                     total_tokens=cost.total_tokens, prompt_tokens=cost.prompt_tokens,
                     completion_tokens=cost.completion_tokens, total_cost=cost.total_cost,
                     query_date=query_date,query_time=query_time, 
                     response_time=response_time
                     )
        session = SessionLocal()
        session.add(db)
        session.commit()
        session.refresh(db)
        session.close()

    @staticmethod
    def delete_sess_db(session_id):
        session = SessionLocal()
        query = session.query(QueryDB).filter(QueryDB.session_id == session_id)
        result = query.delete()
        session.commit()
        session.close()

        if result == 0:
            raise HTTPException(status_code=404, detail=f"Session id {session_id} not found")

        return {'message': f"Session id {session_id} Deleted"}
