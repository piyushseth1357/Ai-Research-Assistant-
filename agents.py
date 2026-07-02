from crewai import Agent, LLM
import os
from dotenv import load_dotenv
import litellm

load_dotenv()

# ============================================
# Groq Cache Fix — Sync + Async Patch
# ============================================
def remove_cache(kwargs):
    if 'messages' in kwargs:
        for msg in kwargs['messages']:
            if isinstance(msg, dict):
                msg.pop('cache_breakpoint', None)
                msg.pop('cache_control', None)
                content = msg.get('content', [])
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict):
                            item.pop('cache_control', None)
                            item.pop('cache_breakpoint', None)
    kwargs.pop('cache_breakpoint', None)
    kwargs.pop('cache_control', None)                        

_orig_completion = litellm.completion
_orig_acompletion = litellm.acompletion

def _patched_completion(*args, **kwargs):
    remove_cache(kwargs)
    return _orig_completion(*args, **kwargs)

async def _patched_acompletion(*args, **kwargs):
    remove_cache(kwargs)
    return await _orig_acompletion(*args, **kwargs)

litellm.completion = _patched_completion
litellm.acompletion = _patched_acompletion

# ============================================
# Internet Check
# ============================================
def internet_hai():
    try:
        import urllib.request
        import socket
        # timeout = 3 seconds
        urllib.request.urlopen("https://www.google.com", timeout=3)
        return True
    except (urllib.error.URLError, socket.gaierror, Exception):
        return False

# ============================================
# LLM Setup
# ============================================
if internet_hai():
    print("🌐 Internet mila! Groq use ho raha hai!")
    my_llm = LLM(
        model="groq/llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7
    )
else:
    print("📵 Internet nahi! Ollama use ho raha hai!")
    my_llm = LLM(
        model="ollama/qwen2:0.5b",
        base_url="http://localhost:11434",
    )

# ============================================
# Agents
# ============================================
researcher = Agent(
    role="Expert Researcher",
    goal="Diye gaye topic ke baare mein bahut detailed aur accurate information nikalo",
    backstory="""
        Tum duniya ke best researcher ho.
        Tumhare paas kisi bhi topic ko 
        deeply analyze karne ki power hai.
    """,
    llm=my_llm,
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role="Professional Report Writer",
    goal="Research information ko ek clear professional report mein likho",
    backstory="""
        Tum ek experienced professional writer ho.
        Tum complex information ko simple 
        language mein explain karna jaante ho.
    """,
    llm=my_llm,
    verbose=True,
    allow_delegation=False
)