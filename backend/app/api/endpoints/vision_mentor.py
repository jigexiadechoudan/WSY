from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.services.pose_analysis_service import pose_extractor
from app.services.standard_pose_library import pose_library
from app.services.pose_comparator import pose_comparator

router = APIRouter()

class PoseLandmark(BaseModel):
    x: float
    y: float
    z: float
    visibility: float

class AnalyzePoseRequest(BaseModel):
    landmarks: List[PoseLandmark]
    target_pose: str = "orchid_hand_left" # Default pose to check

class AnalyzePoseResponse(BaseModel):
    score: int
    feedback: List[str]
    details: Dict[str, float]
    status: str

@router.post("/analyze-pose", response_model=AnalyzePoseResponse)
async def analyze_pose(data: AnalyzePoseRequest):
    """
    Analyze user pose for Opera movements.
    Input: MediaPipe Pose Landmarks (33 points)
    Output: Similarity score and correction feedback
    """
    if not data.landmarks or len(data.landmarks) < 33:
        raise HTTPException(status_code=400, detail="Invalid landmarks data")

    # 1. Extract features from landmarks
    # Convert Pydantic models to list of dicts for service
    landmarks_list = [l.dict() for l in data.landmarks]
    features = pose_extractor.extract_features(landmarks_list)
    
    if not features:
        raise HTTPException(status_code=500, detail="Feature extraction failed")

    # 2. Compare with target pose
    score, feedback, details = pose_comparator.compare_pose(features, data.target_pose)

    return {
        "score": score,
        "feedback": feedback,
        "details": details,
        "status": "success"
    }

@router.get("/poses")
async def get_available_poses():
    """
    List all available standard poses for practice.
    """
    return {"poses": pose_library.list_poses()}

@router.get("/history")
async def get_practice_history():
    """
    Get user practice history.
    """
    return {"history": []}
