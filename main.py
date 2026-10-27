import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="AI Comic Backend Cloud MVP")

# 允许跨域请求，适配手机端网页访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScriptRequest(BaseModel):
    text: str

@app.post("/api/split-script")
def split_script(req: ScriptRequest):
    text = req.text.strip()
    if not text:
        return {"success": False, "message": "剧本内容不能为空"}
    
    # 模拟智能分镜解析
    sentences = [s.strip() for s in text.replace("！", "。").replace("？", "。").split("。") if s.strip()]
    
    storyboard = []
    for i, sent in enumerate(sentences, 1):
        storyboard.append({
            "scene_id": i,
            "visual": f"画面描述: 角色处于剧情关键场景中，表现出符合【{sent}】的动作与神态。",
            "dialogue": sent,
            "image_url": f"https://picsum.photos/400/250?random={i}"
        })
        
    return {
        "success": True,
        "total_scenes": len(storyboard),
        "storyboard": storyboard
    }

if __name__ == "__main__":
    import uvicorn
    # 动态获取云端平台（如 Render）分配的端口
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

