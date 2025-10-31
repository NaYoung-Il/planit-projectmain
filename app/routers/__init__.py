from fastapi import APIRouter
from . import review, comment, like, photo
from . import city_router, trip_router, weather
from . import user

router = APIRouter()
# #1.기능별 등록               1,2,3 중에 골라주세요
# #user
# router.include_router(user.router)
# # trip  
# # trip_router: Trip, TripDay, Schedule, ChecklistItem
# # city_router: City, Place
# for module in [city_router,trip_router]:
#     router.include_router(module.router)

# #review : review, comment, like, photo
# for module in [review,comment,like,photo]:
#     router.include_router(module.router)

# 2. 통합
planit = [user,city_router,trip_router,review,comment,like,photo,weather]
for module in planit:
    router.include_router(module.router)


# import importlib
# import pkgutil

# # 3. gpt - 동적 자동스캔방식
# for _, module_name, _ in pkgutil.iter_modules(__path__):
#     module = importlib.import_module(f"{__name__}.{module_name}")
#     if hasattr(module, "router"):
#         router.include_router(module.router)