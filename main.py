import os
import openai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-wordpress-site.com"],  # Adjust this to your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VeganizeRequest(BaseModel):
    recipe: str

@app.post("/veganize")
async def veganize(data: VeganizeRequest):
    prompt = f"""Please veganize the following recipe or ingredients. 
    Provide a plant-based version by swapping non-vegan ingredients with plant-based alternatives and updating instructions if necessary:\n\n{data.recipe}"""

    try:
        response = openai.chat.completions.create(
            model='gpt-4',
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        result = response.choices[0].message['content'].strip()
        return {"veganized": result}

    except Exception as e:
        raise HTTPException(500, detail=str(e))
