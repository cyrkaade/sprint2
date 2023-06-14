from fastapi import Depends, HTTPException, Response
from datetime import datetime
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router



@router.post("/{shanyrak_id}/comments")
def create_comment(
    shanyrak_id: str,
    content: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    # Create a new comment
    comment = {
        "content": content,
        "created_at": datetime.now(),
        "author_id": str(jwt_data.user_id),
    }
    svc.repository.add_comment(shanyrak_id, comment)

    return Response(status_code=201)
