from fastapi import APIRouter
from app.dal import DAL

router = APIRouter(
    prefix="/queries"
)

dal = DAL()

@router.get("/query_1")
def get_high_priority_targets():
    """High priority targets with movement over 5 km"""
    return dal.get_high_priority_targets()