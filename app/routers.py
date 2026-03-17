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

@router.get("/query_2")
def count_signal_types():
    """Show count of each signal type"""
    return dal.count_signal_types()

@router.get("/query_3")
def most_entity():
    """3 most appearing UNKNOWN entity"""
    return dal.most_entity()

