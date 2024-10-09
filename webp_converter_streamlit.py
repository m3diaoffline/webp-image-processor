import streamlit as st
from PIL import Image
import os
import zipfile
import tempfile
from io import BytesIO

def convert_and_zip(images):
    with tempfile.TemporaryDirectory() as temp_dir:
        converted_files = []
        total_files = len(images)

        # Initialize progress bar
        progress = st.progress(0)

        for i, image_file in enumerate(images):
            try:
                # Open the image
                image = Image.open(image_file)
                
                # Resize the image if it's too large
                if resize and (image.width > 2000 or image.height > 2000):
                    image.thumbnail((2000, 2000))
                
                filename = os.path.splitext(image_file.name)[0] + '.webp'
                webp_path = os.path.join(temp_dir, filename)

                # Save the image as WEBP
                image.save(webp_path, 'WEBP')
                converted_files.append(webp_path)
            except Exception as e:
                st.error(f"Error processing {image_file.name}: {e}")

            # Update the progress bar
            progress.progress((i + 1) / total_files)

        # Create a zip file containing all converted files
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for file_path in converted_files:
                zip_file.write(file_path, os.path.basename(file_path))

        # Prepare the zip file for download
        zip_buffer.seek(0)
        return zip_buffer

def main():
    # Profile photo for branding
    st.image("m3dia_offline_profile.png", width=50)

    st.write("by m3dia_offline", unsafe_allow_html=True)

    st.title("WEBP Image Converter")
    st.write("Upload your JPEG or PNG images and convert them to WEBP format")

    # Set a cap on the number of files users can upload at once
    uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    # Limit the number of uploads to prevent memory overload
    if uploaded_files and len(uploaded_files) > 50:
        st.error("You can upload a maximum of 50 images at a time.")
        return

    if st.button("Convert and Download") and uploaded_files:
        zip_buffer = convert_and_zip(uploaded_files)

    if len(uploaded_files) > 100:  # Adjust the number based on your environment's capacity
        st.error("Please upload a maximum of 100 images at a time.")
        return

        st.download_button(
            label="Download ZIP",
            data=zip_buffer,
            file_name="converted_images.zip",
            mime="application/zip"
        )

# The function call needs to be at the main level of the script
if __name__ == "__main__":
    main()
