import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Set your API key directly (Not recommended for production!)
openai.api_key = "XYZ"

app = FastAPI()

# Allow requests from your website's domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://veganizin'],  # Update if your domain is a full URL, e.g.: 'https://veganizin.com'
    allow_methods=['POST', 'GET', 'PUT', 'DELETE', 'OPTIONS'],
    allow_headers=['*'],
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
