from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from recommendations import recommend_courses  # Ensure this is your course recommendation function

# Create FastAPI instance
app = FastAPI()

# Set up templates directory
templates = Jinja2Templates(directory="templates")

class UserRequest(BaseModel):
    user_id: int
    desired_skills: List[str]

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "recommendations_html": ""})

@app.post("/recommendations/", response_class=HTMLResponse)
async def get_recommendations(request: Request, desired_skills: str = Form(...)):
    # Process skills from the form
    recommendations = recommend_courses(desired_skills)  # Ensure this returns a DataFrame
    recommendations_list = recommendations.to_dict(orient='records')

    # Build HTML response with recommendations
    recommendations_html = "<h2>Recommendations:</h2><ul>"
    for course in recommendations_list:
        recommendations_html += f"<li>{course['course_title']} - {course['platform']}</li>"
    recommendations_html += "</ul>"

    # Return the form with recommendations
    return templates.TemplateResponse("form.html", {"request": request, "recommendations_html": recommendations_html})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
