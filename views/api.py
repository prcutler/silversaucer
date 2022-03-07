import fastapi
from fastapi_chameleon import template

router = fastapi.APIRouter()


@router.get("/api/album")
def today():
    return {
        "album": "Like a Prayer",
        "artist": "Madonna",
        "url": "https://i.discogs.com/6UaW3D3DWavkDhoC4JY5B4pVATBWNsZUBaUKRPqe_0A/rs:fit/g:sm/q:90/h:600/w:600/czM6Ly9kaXNjb2dz/LWltYWdlcy9SLTEw/ODc2NjMtMTI4OTA4/MjkyNC5qcGVn.jpeg"
    }
