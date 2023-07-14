from pdfreader import SimplePDFViewer
import os
import pdfplumber

def pdf_to_txt(pdf_file_path, txt_file_path):
    # Open the PDF file
    with pdfplumber.open(pdf_file_path) as pdf:
        # Initialize an empty string to store the extracted text
        extracted_text = ''

        # Loop over each page in the PDF
        for page in pdf.pages:
            # Extract the text from the page
            page_text = page.extract_text()

            # Append the page text to the extracted text
            extracted_text += ' ' + page_text

    # Write the extracted text to a text file
    with open(txt_file_path, 'w') as txt_file:
        txt_file.write(extracted_text)


def convert_pdf_to_txt(file_path):
    # Open the PDF file in read-binary mode
    with open(file_path, 'rb') as file:
        # Create a PDF file viewer object
        viewer = SimplePDFViewer(file)

        # Initialize an empty string to hold the extracted text
        text = ''

        # Loop through each page in the PDF and extract the text
        for canvas in viewer:
            viewer.render()
            text += ''.join(viewer.canvas.strings)

    # Create the Texts directory if it doesn't exist
    if not os.path.exists('Texts'):
        os.makedirs('Texts')

    # Write the extracted text to a .txt file in the Texts directory
    with open('Texts/output1.txt', 'w') as output_file:
        output_file.write(text)

# Call the function with the path to your PDF file
convert_pdf_to_txt("PDFs/WUDC_manual.pdf")
pdf_to_txt("PDFs/WUDC_manual.pdf", "Texts/output2.txt")

