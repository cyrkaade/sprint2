from fastapi import Depends, HTTPException, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


@router.get("/{shanyrak_id}/comments")
def get_comments(
    shanyrak_id: str,
    svc: Service = Depends(get_service),
) -> dict[str, list]:
    shanyrak = svc.repository.get_shanyrak(shanyrak_id)
    if shanyrak and "comments" in shanyrak:
        comments = shanyrak["comments"]
        return {"comments": comments}

    return {"comments": []}
