from fastapi import APIRouter, HTTPException

from app.models import Option, Question
from app.dependencies import db_dep
from app.schemas import OptionCreate, OptionUpdate, OptionGetResponse, OptionGetDetailResponse



router = APIRouter(
    prefix="/options",
    tags=["options"],
)



@router.get("/", response_model = list[OptionGetResponse])
async def get_options(db:db_dep):
    return db.query(Option).all()


@router.get("/{id}/", response_model = OptionGetDetailResponse)
async def get_option(id: int, db: db_dep):
    option = db.query(Option).filter(Option.id == id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Option not found")

    return option


@router.post("/create/", response_model = OptionGetDetailResponse)
async def create_option(
        option: OptionCreate,
        db: db_dep,

):
    if not db.query(Question).filter(Question.id == option.id).first():
        raise HTTPException(status_code=400, detail="Invalid Question ID")

    existing_correct_option = db.query(Option).filter(
        Option.question_id == option.question_id,
        Option.is_correct == True,
    )

    if existing_correct_option and option.is_correct:
        raise HTTPException(status_code=400, detail="Question already has a correct option")

    new_option = Option(
        **option.model_dump(),
    )

    db.add(new_option)
    db.commit()
    db.refresh(new_option)

    return new_option


@router.put("/update/{id}/", response_model = OptionGetDetailResponse)
async def update_option(
        id: int,
        option: OptionUpdate,
        db: db_dep,

):
    db_option = db.query(Option).filter(Option.id == id).first()
    if not db_option:
        raise HTTPException(status_code=404, detail="Option not found")

    for key, value in option.model_dump(exclude_unset=True).items():
        setattr(db_option, key, value)

    db.commit()
    db.refresh(db_option)

    return db_option


@router.delete("/delete/{id}/")
async def delete_option(
        id: int,
        db: db_dep,

):
    db_option = db.query(Option).filter(Option.id == id).first()
    if not db_option:
        raise HTTPException(status_code=404, detail="Option not found")

    db.delete(db_option)
    db.commit()

    return {
        "option ID": id,
        "detail": "Option deleted successfully",
    }