import tkinter as tk
import customtkinter
from pytube import YouTube

def previewDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink)
        streams = ytObject.streams
        res = [stream.resolution for stream in streams.filter(progressive=True)]
        resolutionsOptions.configure(state= 'normal', values=res)
        previewStatus_label.configure(state= 'normal', text = 'Title: ' + ytObject.title, text_color = 'black')

    except:
        previewStatus_label.configure(text='Invalid link for Preview', text_color = 'red')

def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        resolution = resolutionsOptions.get()
        video = ytObject.streams.filter(progressive=True, res=resolution).first()
        #video = ytObject.streams.get_highest_resolution()
        finishedLabel.configure (text = '')
        video.download()
        finishedLabel.configure(state='normal', text='Downloaded complete: '+ytObject.title)
        restart_button.configure(text='Restart')
        

    except:
        finishedLabel.configure(text='Download Failed.', text_color = 'red')
        restart_button.configure(text='Restart')

def restart():
    previewStatus_label.configure(state= 'normal', text = ' ', text_color = 'black')
    finishedLabel.configure(state='normal', text=' ')
    resolutionsOptions.configure(state= 'disabled', values=[])
    url_var.set('')
    resolution_var.set("Select Resolution")
    restart_button.configure(text = 'Cancel')

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size-bytes_remaining
    percent_complete = bytes_downloaded/total_size *100
    per = str(int(percent_complete))
    progress_perc.configure(text=per + '%')
    progress_perc.update()
    progress_bar.set(float(percent_complete)/100)
    


# System Settings
customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')

# App Frame
app = customtkinter.CTk()
app.geometry("720x380")
app.title('YouTube Downloader')

# UI Elements



# Create preview_frame to house the YouTube link's text box and preview button
preview_frame = customtkinter.CTkFrame(master=app)

title = customtkinter.CTkLabel(master=preview_frame, text='Link')
title.pack(side = 'left', padx=5, pady=15)

url_var = tk.StringVar()
link = customtkinter.CTkEntry(master = preview_frame, width=350, height=30, textvariable=url_var)
link.pack(side = 'left', padx = 5, pady=5)
preview_button = customtkinter.CTkButton(master = preview_frame, text='Preview', command=previewDownload)
preview_button.pack(side='left', padx=10)
preview_frame.pack(side='top', pady = 25)
# End of preview_frame

# Preview status message
previewStatus_label = customtkinter.CTkLabel(master= app, text="")
previewStatus_label.pack(pady=5)

# Create Combo box for video resolution options
resolution_var = customtkinter.StringVar(value="Select Resolution")
resolutionsOptions = customtkinter.CTkComboBox(master=app, state='disabled', variable = resolution_var)
resolutionsOptions.pack(pady=10)

# Create options_frame to house the Download and Cancel button
options_frame = customtkinter.CTkFrame(master= app)
download_button = customtkinter.CTkButton(master=options_frame, text='Download', command=startDownload)
download_button.pack(side='left', pady=10, padx=15)
restart_button = customtkinter.CTkButton(master=options_frame, text='Cancel', command=restart)
restart_button.pack(side='left', pady=10, padx=15)
options_frame.pack()
# End of options_frame


progress_perc = customtkinter.CTkLabel(master=app, text ='0%' )
progress_perc.pack()
progress_bar = customtkinter.CTkProgressBar(app, width=400)
progress_bar.set(0)
progress_bar.pack(padx=10, pady=10)


finishedLabel = customtkinter.CTkLabel(app, text="")
finishedLabel.pack()





# Run app
app.mainloop()