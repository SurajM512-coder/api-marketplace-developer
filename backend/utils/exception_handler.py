from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException



async def http_exception_handler(
    request: Request,
    exc: HTTPException
):

    return JSONResponse(
        status_code=exc.status_code,

        content={
            "success": False,
            "message": exc.detail
        }
    )




async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    return JSONResponse(
        status_code=422,

        content={
            "success": False,
            "message": "Invalid request data",
            "errors": exc.errors()
        }
    )