import os

def save_pdf_to_directory(uploaded_file, directory):
    if uploaded_file is not None:
        # Define directory to save file
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Save uploaded PDF file to directory
        with open(os.path.join(directory, uploaded_file.name), "wb") as pdf_file:
            pdf_file.write(uploaded_file.getbuffer())
        
        st.success(f"File '{uploaded_file.name}' saved successfully!")


