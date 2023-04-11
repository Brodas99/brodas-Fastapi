from fastapi import APIRouter
from app.api.routes.cleaning.cleanings import router as cleanings_router
from app.api.routes.users.users import router as user_router


router = APIRouter()
router.include_router(cleanings_router, prefix="/cleanings", tags=["cleanings"])
router.include_router(user_router, prefix='/user', tags=["users"])