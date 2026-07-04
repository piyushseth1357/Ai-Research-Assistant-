from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, StreamingResponse
import uvicorn
import os
import glob
import json
import asyncio
import ollama
import concurrent.futures
import fitz  # PyMuPDF
import urllib.parse
import urllib.request
import socket
import litellm
import random
import base64
import requests
from urllib.parse import quote
from io import BytesIO
from PIL import Image

def internet_hai():
    try:
        urllib.request.urlopen("https://www.google.com", timeout=3)
        return True
    except (urllib.error.URLError, socket.gaierror, Exception):
        return False

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/status")
async def status():
    online = internet_hai()
    return {
        "online": online,
        "mode": "Groq (Online)" if online else "Ollama (Offline)"
    }

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return StreamingResponse(BytesIO(b""), media_type="image/x-icon")

@app.get("/reports")
async def get_reports():
    files = glob.glob("report_*.txt")
    reports = []
    for f in sorted(files, reverse=True):
        try:
            with open(f, "r", encoding="utf-8") as file:
                content = file.read()
            reports.append({
                "filename": f,
                "name": f.replace("report_","").replace(".txt","").replace("_"," "),
                "preview": content[:200]
            })
        except:
            pass
    return {"reports": reports}

@app.get("/report/{filename}")
async def get_report(filename: str):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return {"content": f.read()}
    except:
        return {"content": "Report not found!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Check if it is an image
        if file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
            image_data = await file.read()
            import base64
            img_b64 = base64.b64encode(image_data).decode("utf-8")
            ext = file.filename.split('.')[-1].lower()
            return {
                "success": True, 
                "is_image": True, 
                "image_data": f"data:image/{ext};base64,{img_b64}"
            }
            
        content = ""
        if file.filename.lower().endswith(".pdf"):
            pdf_data = await file.read()
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            for page in doc:
                content += page.get_text() + "\n"
        else:
            # Assume text file
            content = (await file.read()).decode("utf-8", errors="ignore")
        return {"success": True, "is_image": False, "extracted_text": content}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/ask")
async def ask_endpoint(prompt: str = Form(...), file: UploadFile = File(None)):
    online = await asyncio.to_thread(internet_hai)
    file_bytes = None
    is_image = False
    
    if file and file.filename:
        file_bytes = await file.read()
        is_image = file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif'))

    async def event_generator():
        try:
            yield f"data: {json.dumps({'type': 'status', 'msg': '🧠 Analyzing your request...'})}\n\n"
            await asyncio.sleep(0.1)
            
            intents = {"chat": True, "research": False, "image_gen": False, "image_edit": False}
            
            if online:
                # Fast path for simple greetings/chat to save time
                lower_prompt = prompt.lower()
                fast_path_words = ["research", "report", "generate", "image", "photo", "pic", "draw", "create", "change background", "edit"]
                if not is_image and len(prompt.split()) <= 8 and not any(w in lower_prompt for w in fast_path_words):
                    intents["chat"] = True
                else:
                    router_prompt = f"""
                    Analyze the user's request: '{prompt}'.
                    Is an image file attached? {'Yes' if is_image else 'No'}.
                    
                    Return ONLY a valid JSON object with boolean values (true/false) for these keys, and nothing else:
                    - "chat": true if the request is conversational, a greeting, or simple question.
                    - "research": true if the request asks for a detailed report, essay, code script, or deep explanation about a topic.
                    - "image_gen": true if the request asks to generate, create, or draw a new picture/image.
                    - "image_edit": true if an image is attached AND the user asks to change, edit, or modify it (like changing background).
                    
                    Example output format:
                    {{"chat": false, "research": true, "image_gen": true, "image_edit": false}}
                    """
                    try:
                        router_response = await litellm.acompletion(
                            model="groq/llama-3.1-8b-instant",
                            api_key=os.getenv("GROQ_API_KEY"),
                            messages=[{'role': 'user', 'content': router_prompt}],
                            response_format={"type": "json_object"}
                        )
                        parsed_intents = json.loads(router_response.choices[0].message.content)
                        intents["chat"] = parsed_intents.get("chat", False)
                        intents["research"] = parsed_intents.get("research", False)
                        intents["image_gen"] = parsed_intents.get("image_gen", False)
                        intents["image_edit"] = parsed_intents.get("image_edit", False)
                        if not any(intents.values()):
                            intents["chat"] = True
                            
                        # Prevent overlapping output: if doing image tasks, disable text tasks
                        if intents["image_gen"] or intents["image_edit"]:
                            intents["chat"] = False
                            intents["research"] = False
                    except:
                        pass
            
            if not online:
                intents["research"] = True
                intents["chat"] = False
    
            yield f"data: {json.dumps({'type': 'stream_start', 'intents': intents})}\n\n"
            
            queue = asyncio.Queue()
            running_loop = asyncio.get_running_loop()
            
            def run_image_task():
                try:
                    if intents["image_edit"] and is_image:
                        asyncio.run_coroutine_threadsafe(queue.put({"type": "chunk", "content": "\n\n> ⏳ **Status:** Removing background with High Quality Matting..."}), running_loop)
                        from rembg import remove
                        # Use alpha matting for much smoother, realistic edges
                        foreground_bytes = remove(
                            file_bytes, 
                            alpha_matting=True, 
                            alpha_matting_foreground_threshold=240,
                            alpha_matting_background_threshold=10,
                            alpha_matting_erode_size=10
                        )
                        foreground_img = Image.open(BytesIO(foreground_bytes)).convert("RGBA")
                        
                        bg_desc = prompt
                        if online:
                            try:
                                bg_response = litellm.completion(
                                    model="groq/llama-3.1-8b-instant",
                                    api_key=os.getenv("GROQ_API_KEY"),
                                    messages=[{'role': 'user', 'content': f"Extract ONLY the requested background visual description from this prompt: '{prompt}'. Reply with max 5 words. Do not explain anything."}]
                                )
                                bg_desc = bg_response.choices[0].message.content.strip()
                            except: pass
                        
                        asyncio.run_coroutine_threadsafe(queue.put({"type": "chunk", "content": f"\n\n> ⏳ **Status:** Generating 4K Realistic Background: *{bg_desc}*..."}), running_loop)
                        
                        # Add realistic tags to make it look high quality
                        enhanced_bg_prompt = f"{bg_desc}, ultra realistic, 8k resolution, photorealistic, professional photography, highly detailed"
                        encoded_bg_prompt = quote(enhanced_bg_prompt)
                        
                        w, h = foreground_img.size
                        # If image is too small, upscale it for better quality
                        if w < 512 or h < 512:
                            ratio = max(512/w, 512/h)
                            w = int(w * ratio)
                            h = int(h * ratio)
                            foreground_img = foreground_img.resize((w, h), Image.Resampling.LANCZOS)
                            
                        max_dim = 1080
                        if w > max_dim or h > max_dim:
                            ratio = min(max_dim/w, max_dim/h)
                            w = int(w * ratio)
                            h = int(h * ratio)
                            foreground_img = foreground_img.resize((w, h), Image.Resampling.LANCZOS)
                        
                        bg_url = f"https://image.pollinations.ai/prompt/{encoded_bg_prompt}?seed={random.randint(1,999999)}&width={w}&height={h}&nologo=true&nofeed=true"
                        headers = {"User-Agent": "Mozilla/5.0"}
                        bg_req = requests.get(bg_url, headers=headers, timeout=30)
                        
                        background_img = Image.open(BytesIO(bg_req.content)).convert("RGBA")
                        background_img = background_img.resize((w, h), Image.Resampling.LANCZOS)
                        
                        # Composite with alpha blending
                        final_img = Image.alpha_composite(background_img, foreground_img)
                        
                        output_buffer = BytesIO()
                        final_img.convert("RGB").save(output_buffer, format="JPEG", quality=100)
                        img_base64 = base64.b64encode(output_buffer.getvalue()).decode()
                        
                        asyncio.run_coroutine_threadsafe(queue.put({"type": "chunk", "content": "\n\n> ✅ **Status:** Image editing complete!"}), running_loop)
                        asyncio.run_coroutine_threadsafe(queue.put({"type": "image", "url": f"data:image/jpeg;base64,{img_base64}", "caption": f"✨ Background changed to: {bg_desc}"}), running_loop)
                    
                    elif intents["image_gen"]:
                        asyncio.run_coroutine_threadsafe(queue.put({"type": "chunk", "content": "\n\n> ⏳ **Status:** Generating requested image..."}), running_loop)
                        desc = prompt
                        if online:
                            try:
                                gen_response = litellm.completion(
                                    model="groq/llama-3.1-8b-instant",
                                    api_key=os.getenv("GROQ_API_KEY"),
                                    messages=[{'role': 'user', 'content': f"Extract ONLY the visual description of the image to generate from this prompt: '{prompt}'. Reply with max 10 words. Do not explain anything."}]
                                )
                                desc = gen_response.choices[0].message.content.strip()
                            except: pass
                            
                        encoded_prompt = quote(desc)
                        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={random.randint(1,999999)}&width=1024&height=1024&nologo=true&nofeed=true"
                        headers = {"User-Agent": "Mozilla/5.0"}
                        resp = requests.get(url, headers=headers, timeout=25)
                        if resp.status_code == 200:
                            img_base64 = base64.b64encode(resp.content).decode()
                            asyncio.run_coroutine_threadsafe(queue.put({"type": "chunk", "content": "\n\n> ✅ **Status:** Image generation complete!"}), running_loop)
                            asyncio.run_coroutine_threadsafe(queue.put({"type": "image", "url": f"data:image/jpeg;base64,{img_base64}", "caption": f"🎨 Generated: {desc}"}), running_loop)
                except Exception as e:
                    asyncio.run_coroutine_threadsafe(queue.put({"type": "chunk", "content": f"\n\n❌ **[Image Task Failed]:** {str(e)}"}), running_loop)
    
            def run_text_task():
                try:
                    text_prompt = prompt
                    if intents["research"]:
                        text_prompt = f"Topic: {prompt}\n\nNote: Please correct any spelling mistakes automatically.\n\nNeeche diye format mein professional research report likho:\n\n📌 OVERVIEW\n(Topic ka introduction)\n\n🔑 KEY POINTS\n(5-7 important points)\n\n💼 REAL WORLD USE\n(Examples)\n\n✅ BENEFITS\n(Fayde)\n\n🚀 FUTURE SCOPE\n(Aage kya hoga)\n\n📝 CONCLUSION\n(Final thoughts)"
                    elif intents["chat"]:
                        text_prompt = f"You are a helpful, friendly AI assistant. Reply naturally, directly, and conversationally to: '{prompt}'"
                        
                    if online:
                        stream = litellm.completion(
                            model="groq/llama-3.1-8b-instant",
                            api_key=os.getenv("GROQ_API_KEY"),
                            messages=[{'role': 'user', 'content': text_prompt}],
                            stream=True
                        )
                        for chunk in stream:
                            content = chunk.choices[0].delta.content or ""
                            if content:
                                asyncio.run_coroutine_threadsafe(queue.put({"type": "chunk", "content": content}), running_loop)
                    else:
                        stream = ollama.chat(model='qwen2:0.5b', messages=[{'role': 'user', 'content': text_prompt}], stream=True)
                        for chunk in stream:
                            content = chunk['message']['content']
                            asyncio.run_coroutine_threadsafe(queue.put({"type": "chunk", "content": content}), running_loop)
                except Exception as e:
                    import traceback
                    asyncio.run_coroutine_threadsafe(queue.put({"type": "chunk", "content": f"\n\n❌ **[Text Task Failed]:** {str(e)} \n\n {traceback.format_exc()}"}), running_loop)
    
            import threading
            tasks_to_wait = 0
            if intents["chat"] or intents["research"]:
                tasks_to_wait += 1
                threading.Thread(target=lambda: (run_text_task(), asyncio.run_coroutine_threadsafe(queue.put(None), running_loop))).start()
            
            if intents["image_gen"] or intents["image_edit"]:
                tasks_to_wait += 1
                threading.Thread(target=lambda: (run_image_task(), asyncio.run_coroutine_threadsafe(queue.put(None), running_loop))).start()
    
            if tasks_to_wait == 0:
                queue.put_nowait(None)
                
            completions = 0
            full_text = ""
            try:
                while completions < tasks_to_wait:
                    item = await asyncio.wait_for(queue.get(), timeout=300)
                    if item is None:
                        completions += 1
                        continue
                    if item["type"] == "chunk":
                        full_text += item["content"]
                    yield f"data: {json.dumps(item)}\n\n"
            except asyncio.TimeoutError:
                err_msg = "\\n\\n❌ **[Error]:** Request timed out after 5 minutes. If this is your first time removing a background, it might take a while to download the AI model. Please try again."
                yield f"data: {json.dumps({'type': 'chunk', 'content': err_msg})}\n\n"
            except Exception as e:
                err_msg = f"\\n\\n❌ **[Server Error]:** {str(e)}"
                yield f"data: {json.dumps({'type': 'chunk', 'content': err_msg})}\n\n"
                
            if full_text and (intents["research"] or intents["chat"]):
                safe = prompt[:20].replace(" ", "_").replace("/", "").replace("\\", "")
                if not safe: safe = "chat"
                fname = f"report_{safe}_{random.randint(1000,9999)}.txt"
                with open(fname, "w", encoding="utf-8") as f:
                    f.write(f"TOPIC: {prompt}\n{'='*50}\n\n{full_text}")
                yield f"data: {json.dumps({'type': 'save', 'filename': fname})}\n\n"
    
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
        except Exception as outer_e:
            import traceback
            err_msg = f"\\n\\n❌ **[CRITICAL STREAM ERROR]:** {str(outer_e)} \\n\\n {traceback.format_exc()}"
            yield f"data: {json.dumps({'type': 'chunk', 'content': err_msg})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    os.makedirs("templates", exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)