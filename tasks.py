from crewai import Task
from agents import researcher, writer


def create_research_task(topic):
    task = Task(
        description=f"""
        Neeche diye topic pe detailed research karo:
        
        TOPIC: {topic}
        
        In 5 cheezein zarur dhundo:
        1. Topic kya hai - simple explanation mein
        2. Iske main important points kya hain
        3. Real world mein iska use kahan hota hai
        4. Iske fayde (Benefits) kya hain
        5. Future mein iska kya scope hai
        
        Sab kuch clear aur structured format mein likho.
        """,
        expected_output="""
        Ek detailed research document jisme:
        - Topic ka clear overview ho
        - Minimum 5 important points hon
        - Real world examples hon
        - Fayde aur future scope mention ho
        """,
        agent=researcher
    )
    return task


def create_writing_task(topic):
    task = Task(
        description=f"""
        Researcher ne jo research ki hai use lekar
        '{topic}' pe ek professional report banao.
        
        Report exactly is format mein honi chahiye:
        
        ==========================================
        RESEARCH REPORT: {topic}
        ==========================================
        
        📌 OVERVIEW
        (Topic ka 3-4 line mein introduction)
        
        🔑 KEY POINTS
        (5-7 important bullet points)
        
        💼 REAL WORLD APPLICATIONS
        (Kahan use hota hai - examples ke saath)
        
        ✅ BENEFITS & ADVANTAGES
        (Kya kya fayde hain)
        
        🚀 FUTURE SCOPE
        (Aage kya hoga)
        
        📝 CONCLUSION
        (2-3 lines mein final thoughts)
        ==========================================
        """,
        expected_output="""
        Ek complete professional report with all sections filled
        """,
        agent=writer
    )
    return task

def create_code_task(topic):
    task = Task(
        description=f"""
        {topic} ke baare mein 
        working Python code likho with:
        - Complete code
        - Comments explanation
        - Example output
        """,
        expected_output="Complete working Python code with explanation",
        agent=writer
    )
    return task