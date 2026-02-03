import sys
import asyncio
import traceback
import os

# Add local directory to path
sys.path.append(os.getcwd())

try:
    print("Attempting to import main...")
    from main import app, startup_span
    print("Import successful.")

    print("Running startup_span...")
    async def run_startup():
        from helpers.config import get_settings
        settings = get_settings()
        print(f"DEBUG: GENERATION_BACKEND={settings.GENERATION_BACKEND}")
        print(f"DEBUG: EMBEDDING_BACKEND={settings.EMBEDDING_BACKEND}")
        print(f"DEBUG: VECTOR_DB_BACKEND={settings.VECTOR_DB_BACKEND}")
        
        await startup_span()
    
    asyncio.run(run_startup())
    print("Startup successful.")

except Exception as e:
    print(f"Startup failed: {e}")
    traceback.print_exc()
