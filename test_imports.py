import sys
try:
    import streamlit, playwright, google.genai
    print("IMPORTS_OK", sys.executable)
except Exception as e:
    print("IMPORT_ERROR", e)
    raise
