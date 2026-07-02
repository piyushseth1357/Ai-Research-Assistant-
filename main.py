from crewai import Crew, Process
from agents import researcher, writer, my_llm, internet_hai
from tasks import create_research_task, create_writing_task
import ollama
import os

print("\n" + "="*50)
print("   🤖  AI RESEARCH ASSISTANT")
print("   Powered by LLaMA 3 + CrewAI")
print("   Made by: Piyush (BCA Final Year)")
print("="*50 + "\n")

topic = input("📝 Kis topic pe report chahiye? → ")

print(f"\n✅ Topic: {topic}")

if internet_hai():
    print("🌐 Online Mode: Groq (Direct - Fast)")
    print("⏳ Report ban rahi hai...")
    print("-"*50)

    import litellm
    import os
    
    prompt = f'''
    Topic: {topic}
    
    Note: Please correct any spelling mistakes in the topic automatically.
    
    Neeche diye format mein report likho:
    
    📌 OVERVIEW
    (Topic ka introduction)
    
    🔑 KEY POINTS
    (5-7 important points)
    
    💼 REAL WORLD USE
    (Examples)
    
    ✅ BENEFITS
    (Fayde)
    
    🚀 FUTURE SCOPE
    (Aage kya hoga)
    
    📝 CONCLUSION
    (Final thoughts)
    '''
    
    try:
        response = litellm.completion(
            model="groq/llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY"),
            messages=[{'role': 'user', 'content': prompt}]
        )
        result = response.choices[0].message.content
    except Exception as e:
        print(f"⚠️ Groq Error: {str(e)}")
        result = "Error generating report."

else:
    print("📵 Offline Mode: Ollama (Local)")
    print("⏳ Report ban rahi hai...")
    print("-"*50)

    response = ollama.chat(
        model='llama3.2:1b',
        messages=[{
            'role': 'user',
            'content': f'''
            Topic: {topic}
            
            Note: Please correct any spelling mistakes in the topic automatically.
            
            Neeche diye format mein report likho:
            
            📌 OVERVIEW
            (Topic ka introduction)
            
            🔑 KEY POINTS
            (5 important points)
            
            💼 REAL WORLD USE
            (Examples)
            
            ✅ BENEFITS
            (Fayde)
            
            🚀 FUTURE SCOPE
            (Aage kya hoga)
            
            📝 CONCLUSION
            (Final thoughts)
            '''
        }]
    )
    result = response['message']['content']

print("\n" + "="*50)
print("   ✅  REPORT READY!")
print("="*50)
print(result)

safe_topic = topic[:20].replace(" ", "_")
file_name = f"report_{safe_topic}.txt"

with open(file_name, "w", encoding="utf-8") as f:
    f.write(f"TOPIC: {topic}\n")
    f.write("="*50 + "\n\n")
    f.write(str(result))

print(f"\n💾 Report save ho gayi: '{file_name}'")
print("🎉 Complete!\n")