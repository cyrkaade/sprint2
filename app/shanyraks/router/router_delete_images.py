from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router

@router.delete("/{shanyrak_id:str}/media")
def delete_shanyrak_media(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    # Get the shanyrak data from the repository
    shanyrak = svc.repository.get_shanyrak(shanyrak_id)

    # Check if the shanyrak exists and the user has permission to delete the images
    if shanyrak and str(jwt_data.user_id) == str(shanyrak["user_id"]):
        # Delete the images associated with the shanyrak
        update_data = {"photos": []}  # Set the 'photos' field to an empty list to delete all images
        update_result = svc.repository.update_shanyrak(shanyrak_id, jwt_data.user_id, update_data)

        if update_result.modified_count == 1:
            return Response(status_code=200)

    return Response(status_code=404)