from fastapi import Depends, Response, HTTPException

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router


@router.delete("/{shanyrak_id}/comments/{comment_id}")
def delete_comment(
    shanyrak_id: str,
    comment_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    shanyrak = svc.repository.get_shanyrak(shanyrak_id)
    if shanyrak and "comments" in shanyrak:
        comments = shanyrak["comments"]
        for index, comment in enumerate(comments):
            if comment.get("_id") == comment_id and comment.get("author_id") == str(jwt_data.user_id):
                del comments[index]
                svc.repository.update_comment(shanyrak_id, comments)
                return Response(status_code=200)

    raise HTTPException(status_code=404, detail="Comment not found or user is not authorized to delete it")