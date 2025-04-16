from fastapi import APIRouter, HTTPException

from app.models import Topic
from app.dependencies import db_dep, current_user_dep, admin_user_dep
from app.schemas import TopicCreate, TopicGetResponse


router = APIRouter(
    prefix="/topics",
    tags=["/topics"],
)



@router.get("/", response_model=list[TopicGetResponse])
async def get_topics(db: db_dep):
    return db.query(Topic).all()


@router.post("/topics/", response_model=TopicGetResponse)
async def create_topic(
        topic: TopicCreate,
        db: db_dep,
        admin_user: admin_user_dep,
):

    if db.query(Topic).filter(Topic.name == topic.name).first():
        raise HTTPException(status_code=400, detail="Topic already exists")

    new_topic = Topic(
        name=topic.name,
    )
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)

    return {
        "message": "Topic created",
        "topic": topic,
    }


@router.delete("/topic/{id}/")
async def delete_topic(
        id: int,
        db: db_dep,
        admin_user: admin_user_dep,
):
    topic = db.query(Topic).filter(Topic.id == id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    db.delete(topic)
    db.commit()

    return {
        "topic_id": id,
        "message": "Topic deleted",
    }