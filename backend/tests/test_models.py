import os
from dotenv import load_dotenv
from agno.models.openai import OpenAIChat

load_dotenv()

def test_openai_connectivity():
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    
    print(f"Testing OpenAI with Base URL: {base_url}")
    
    model = OpenAIChat(
        id="gpt-4o",
        api_key=api_key,
        base_url=base_url
    )
    
    try:
        response = model.response("Hola, ¿puedes confirmar tu conexión?")
        print("Respuesta del modelo:")
        print(response.content)
        print("\n¡Conexión exitosa!")
    except Exception as e:
        print(f"Error de conexión OpenAI: {e}")

def test_redmine_connectivity():
    from redminelib import Redmine
    url = os.getenv("REDMINE_BASE_URL", "http://cidiia.uce.edu.do/")
    key = os.getenv("REDMINE_API_KEY")
    
    print(f"\nTesting Redmine with URL: {url}")
    if not key:
        print("Error: No se encontró REDMINE_API_KEY")
        return

    try:
        redmine = Redmine(url, key=key)
        # Attempt to get own user details to verify key
        user = redmine.user.get('current')
        print(f"Conexión exitosa a Redmine. Usuario: {user.firstname} {user.lastname}")
    except Exception as e:
        print(f"Error de conexión Redmine: {e}")

if __name__ == "__main__":
    test_openai_connectivity()
    test_redmine_connectivity()
