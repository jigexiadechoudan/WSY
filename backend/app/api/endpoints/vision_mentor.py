from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import math
from app.services.llm_service import LangChainService

router = APIRouter()
llm_service = LangChainService()

class Landmark(BaseModel):
    x: float
    y: float
    z: float

class PoseRequest(BaseModel):
    landmarks: List[List[Landmark]]  # Support multiple hands
    scenario: str  # 'embroidery', 'clay', 'shadow'
    need_feedback: bool = False

def calculate_distance(p1: Landmark, p2: Landmark) -> float:
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

def evaluate_embroidery(hand: List[Landmark]) -> Dict[str, Any]:
    # Su Embroidery: Pinching a needle
    # Thumb (4) and Index (8) should be close
    thumb_tip = hand[4]
    index_tip = hand[8]
    distance = calculate_distance(thumb_tip, index_tip)
    
    # Perfect distance is around 0.02 - 0.05
    if distance < 0.02:
        score = 80
        msg = "捏得太紧了，注意放松。"
    elif distance > 0.15:
        score = max(0, 100 - (distance - 0.15) * 500)
        msg = "手指张得太开了，请捏合食指和拇指。"
    else:
        score = 100 - abs(distance - 0.04) * 200
        msg = "姿势非常标准！"
        
    return {"score": min(100, max(0, int(score))), "hint": msg}

def evaluate_clay(hand: List[Landmark]) -> Dict[str, Any]:
    # Purple Clay: Flat palm for slapping clay
    # All fingertips (8, 12, 16, 20) should be relatively far from wrist (0) and straight
    wrist = hand[0]
    distances = [calculate_distance(wrist, hand[i]) for i in [8, 12, 16, 20]]
    avg_dist = sum(distances) / len(distances)
    
    # Also check if fingers are close to each other (flat hand)
    spread = calculate_distance(hand[8], hand[20])
    
    score = 0
    msg = ""
    if avg_dist < 0.3:
        score = 40
        msg = "手掌没有完全张开，请伸直手指。"
    elif spread > 0.3:
        score = 70
        msg = "手指分得太开了，请并拢手指形成平整的拍子。"
    else:
        score = min(100, avg_dist * 200)
        msg = "手掌平整，发力面积好！"
        
    return {"score": min(100, max(0, int(score))), "hint": msg}

def evaluate_shadow(hand: List[Landmark]) -> Dict[str, Any]:
    # Shadow Puppet: "Rabbit" (兔子)
    # Index (8) and Middle (12) extended. Thumb (4), Ring (16), Pinky (20) pinched together.
    wrist = hand[0]
    # Check extension of index and middle
    d_index = calculate_distance(wrist, hand[8])
    d_middle = calculate_distance(wrist, hand[12])
    
    # Check pinch of thumb, ring, pinky
    d_pinch1 = calculate_distance(hand[4], hand[16])
    d_pinch2 = calculate_distance(hand[4], hand[20])
    
    score = 0
    msg = ""
    if d_index < 0.3 or d_middle < 0.3:
        score = 50
        msg = "请把食指和中指竖直，像兔子的耳朵。"
    elif d_pinch1 > 0.15 or d_pinch2 > 0.15:
        score = 60
        msg = "请把拇指、无名指和小指捏在一起，作为兔子的嘴巴。"
    else:
        score = 90 + (0.15 - max(d_pinch1, d_pinch2)) * 100
        msg = "很棒的兔子手影！"
        
    return {"score": min(100, max(0, int(score))), "hint": msg}

@router.post("/analyze-pose")
async def analyze_pose(request: PoseRequest):
    """
    Analyze user pose for craft learning.
    Input: Skeleton data (MediaPipe)
    Output: Feedback and correction
    """
    if not request.landmarks or len(request.landmarks) == 0:
        return {"status": "waiting", "score": 0, "hint": "未检测到手部", "feedback": None}
        
    hand = request.landmarks[0] # Use the first hand detected
    
    if request.scenario == 'embroidery':
        result = evaluate_embroidery(hand)
    elif request.scenario == 'clay':
        result = evaluate_clay(hand)
    elif request.scenario == 'shadow':
        result = evaluate_shadow(hand)
    else:
        result = {"score": 0, "hint": "未知场景"}
        
    feedback_text = None
    if request.need_feedback and result["score"] >= 85:
        # Generate AI Feedback
        prompt = f"""你是一个非遗文化导师。用户正在体验【{request.scenario}】的动作挑战。
他们做出了非常标准的手势，获得了 {result["score"]} 分的高分！
请用1-2句话（不超过50字）给他们一句带有该非遗文化特色的夸奖。语言要生动、有趣、有文化底蕴。"""
        feedback_text = llm_service.chat([{"role": "user", "content": prompt}])
        
    return {
        "status": "success",
        "score": result["score"],
        "hint": result["hint"],
        "feedback": feedback_text
    }

@router.get("/history")
async def get_practice_history():
    """
    Get user practice history.
    """
    return {"history": []}

