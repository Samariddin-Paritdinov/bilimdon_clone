from fastapi import APIRouter, HTTPException

from app.models import Topic
from app.dependencies import db_dep
router = APIRouter()



@router.post("/topics")
async def create_topic(name: str, db: db_dep):
    query = db.query(Topic).filter(Topic.name == name)
    if query.first():
        raise HTTPException(status_code=400, detail="Topic already exists")
    topic = Topic(name=name)
    db.add(topic)
    db.commit()
    db.refresh(topic)
    

    return {"message": "Topic created", "topic": topic}


@router.delete("/topic/{topic_id}")
async def delete_topic(topic_id: int, db: db_dep):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    db.delete(topic)
    db.commit()

    return {"message": "Topic deleted"}