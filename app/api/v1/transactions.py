from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.db.session import get_db
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionOut

router = APIRouter()


@router.get("/history", response_model=list[TransactionOut])
def transaction_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == "admin":
        return (
            db.query(Transaction)
            .order_by(Transaction.created_at.desc())
            .all()
        )

    return (
        db.query(Transaction)
        .filter(Transaction.buyer_id == current_user.id)
        .order_by(Transaction.created_at.desc())
        .all()
    )