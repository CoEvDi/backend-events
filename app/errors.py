from fastapi import HTTPException
from fastapi.responses import JSONResponse


def HTTPabort(status_code, description):
    raise HTTPException(status_code=status_code, detail=description)


async def server_error(request, exc):
    return JSONResponse(
        status_code=500,
        content={'detail': 'Internal server error'}
    )


async def route_not_found_error(request, exc):
    detail = str(exc.detail)
    if detail == 'Not Found':
        detail = 'Route not found'
    return JSONResponse(
        status_code=404,
        content={'detail': detail}
    )


exception_handlers = {
    500: server_error,
    404: route_not_found_error
}
