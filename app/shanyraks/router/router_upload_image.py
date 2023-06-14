from fastapi import Depends, UploadFile, Response
from typing import List
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router
from ..repository.repository import ShanyrakRepository
from app.utils import AppModel
from app.config import database





@router.post("/{shanyrak_id}/media")
def upload_files(
    shanyrak_id: str,
    files: List[UploadFile],
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    """
    file.filename: str - Название файла
    file.file: BytesIO - Содержимое файла
    """
    

    result = []
    for file in files:
        url = svc.s3_service.upload_file(file.file, file.filename)
        result.append(url)
    update_data = {"photos": result}
    update_result = svc.repository.update_shanyrak(shanyrak_id, jwt_data.user_id, update_data)

    if update_result.modified_count == 1:
        return Response(status_code=200)

    return Response(status_code=404)
    # update_result = svc.repository.update_shanyrak(shanyrak_id, jwt_data.user_id, result)
    # if update_result.modified_count == 1:
    #     return Response(status_code=200)
    # return Response(status_code=404)