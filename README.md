# medical-verifier

medical prescription analyzer

requirements
fastapi
uvicorn[standard]
pydantic
streamlit
google-generativeai
python-dotenv
requests






To run this project, you need to execute two separate components: the FastAPI backend and the Streamlit frontend. First, you must install the required Python libraries.



Installation

You can install the necessary libraries using pip. It's recommended to create a virtual environment first.



FastAPI and uvicorn for the backend:

pip install fastapi uvicorn



Streamlit and requests for the frontend:

pip install streamlit requests



Pydantic for data validation in the backend:

pip install pydantic



<br>



Running the Project

You must run both the backend and frontend simultaneously in separate terminal windows.



1\. Start the Backend

Navigate to the directory containing main.py and run the following command to start the FastAPI server:



uvicorn main:app --reload



main:app specifies that you're running the app object from the main.py file.



--reload enables auto-reloading, so the server restarts automatically when you make changes to the code.



2\. Start the Frontend

In a separate terminal, navigate to the directory containing app.py and run the following command to start the Streamlit application:



streamlit run app.py



After running this command, your web browser should automatically open a new tab with the Streamlit application. If it doesn't, you can manually navigate to the local URL provided in the terminal output, typically http://localhost:8501.

