import customtkinter as ctk
from PIL import Image
import gdown
import pandas as pd


# Function to extract the file ID from the Google Drive link
def extract_file_id(link):
    try:
        return link.split('/d/')[1].split('/')[0]
    except IndexError:
        return None


# Function to download the file from Google Drive and convert to JSON
def download_and_convert_to_json():
    link = link_box.get()
    file_id = extract_file_id(link)
    if not file_id:
        display_code.delete("1.0", "end")
        display_code.insert("1.0", "Invalid Google Drive link. Please enter a valid link.")
        return

    download_link = f"https://drive.google.com/uc?id={file_id}"

    # Use gdown to download the file
    gdown.download(download_link, 'downloaded_file.csv', quiet=False)

    # Convert CSV file to JSON
    df = pd.read_csv('downloaded_file.csv')
    json_data = df.to_json(orient='records')

    # Save JSON file
    with open('data.json', 'w') as json_file:
        json_file.write(json_data)

    display_code.delete("1.0", "end")
    display_code.insert("1.0", "File downloaded and converted to data.json successfully.")

    # Store the file ID for later use
    global stored_file_id
    stored_file_id = file_id


# Function to update the code textbox
def update_code_textbox():
    link = link_box.get()
    file_id = extract_file_id(link)
    if not file_id:
        display_code.delete("1.0", "end")
        display_code.insert("1.0", "Invalid Google Drive link. Please enter a valid link.")
        return

    script_code = f"""
function doGet(e) {{
  var fileId = '{file_id}';
  var file = DriveApp.getFileById(fileId);
  var jsonData = file.getBlob().getDataAsString();

  return ContentService.createTextOutput(jsonData)
      .setMimeType(ContentService.MimeType.JSON);
}}
"""
    display_code.delete("1.0", "end")
    display_code.insert("1.0", script_code)

    # Store the file ID for later use
    global stored_file_id
    stored_file_id = file_id


# Initialize GUI
ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.geometry("1000x600")
app.resizable(False, False)
app.title("API_Gen")
app.config(bg="#2F3E46")

title = ctk.CTkLabel(app, text="API GEN", font=("Libre Barcode 39 text", 65), text_color="#84A98C", bg_color="#2F3E46")
title.place(x=390, y=10)

link_box = ctk.CTkEntry(app, placeholder_text="Enter Google Drive link", text_color="#84A98C", font=("DM Sans", 20),
                        width=460, height=40, corner_radius=10, fg_color="#2F3E46", bg_color="#2F3E46",
                        border_color="#52796F")
link_box.place(x=470, y=125)

download_json = ctk.CTkButton(app, font=("DM Sans Regular", 18), height=35, width=200, corner_radius=8,
                              text="Download .json", text_color="#52796F", bg_color="#2F3E46", fg_color="#CAD2C5",
                              hover_color="#84A98C", command=download_and_convert_to_json)
download_json.place(x=470, y=200)

create_code = ctk.CTkButton(app, font=("DM Sans Regular", 18), height=35, width=250, corner_radius=8,
                            text="Create code to publish API", text_color="#52796F", bg_color="#2F3E46",
                            fg_color="#CAD2C5", hover_color="#84A98C", command=update_code_textbox)
create_code.place(x=680, y=200)

code_label = ctk.CTkLabel(app, text="Code :", font=("DM Sans Regular", 24), text_color="#CAD2C5", bg_color="#2f3e46")
code_label.place(x=470, y=285)

display_code = ctk.CTkTextbox(app, font=("Source Code Pro Regular", 16), width=460, height=250, bg_color="#2F3E46",
                              fg_color="#2f3e46", border_color="#52796F", border_width=3)
display_code.place(x=470, y=320)

step1_label = ctk.CTkLabel(app, font=("DM Sans Regular", 20),
                           text="Step 1: Upload the .csv to your Google Drive and make it public. Copy the link and paste it in the link box",
                           bg_color="#2F3E46", text_color="#CAD2C5", wraplength=380)
step1_label.place(x=40, y=125)

step2_label = ctk.CTkLabel(app, font=("DM Sans Regular", 20), text="Step 2: Click the desired button",
                           bg_color="#2F3E46", text_color="#CAD2C5", wraplength=380)
step2_label.place(x=40, y=225)

step3_label = ctk.CTkLabel(app, font=("DM Sans Regular", 20),
                           text="Step 3: To deploy your API public. Paste the given code in Google Apps Scripts and run it.",
                           bg_color="#2F3E46", text_color="#CAD2C5", wraplength=380)
step3_label.place(x=40, y=275)

success_label = ctk.CTkLabel(app, font=("DM Sans SemiBold Italic", 20),
                             text="WHOA YOU HAVE SUCCESSFULLY DEPLOYED YOUR API.", bg_color="#2F3E46",
                             text_color="#CAD2C5", wraplength=380)
success_label.place(x=60, y=400)

image_path1 = "elements/element-1.png"
png_image1 = ctk.CTkImage(dark_image=Image.open(image_path1), size=(100, 100))
image_label1 = ctk.CTkLabel(app, image=png_image1, text="", bg_color="#2f3e46")
image_label1.place(x=0, y=0)

image_path2 = "elements/element-2.png"
png_image2 = ctk.CTkImage(dark_image=Image.open(image_path2), size=(250, 100))
image_label2 = ctk.CTkLabel(app, image=png_image2, text="", bg_color="#2f3e46")
image_label2.place(x=750, y=0)

app.mainloop()