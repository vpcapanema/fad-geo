from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/api/mock-shapes")
def mock_shapes():
    # 3 shapes fictícios em GeoJSON
    shapes = [
        {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-46.7, -23.5], [-46.6, -23.6], [-46.5, -23.55]]}, "properties": {"nome": "Rodovia Fictícia"}},
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-46.65, -23.52]}, "properties": {"nome": "Sede Município"}},
        {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-46.68, -23.51], [-46.62, -23.53]]}, "properties": {"nome": "Rodovia Estadual"}}
    ]
    return JSONResponse({"shapes": shapes})
