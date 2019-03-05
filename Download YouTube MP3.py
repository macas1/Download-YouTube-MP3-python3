#Requires pafy. Imports-----------------------------------------------
mac = False
try:
  from tkinter import *
  from tkinter import messagebox
except ImportError:
  from Tkinter import *
  import tkMessageBox as messagebox
  mac = True

import pafy, os

#Settings-------------------------------------------------------------
padding = 5

#GUI------------------------------------------------------------------
root = Tk()
root.wm_title("Youtube Audio Downloader - BM")
root.resizable(False, False)
complete = False

def keybind(event):
  run()

def run():
  root.geometry(str(root.winfo_width()) + "x" + str(root.winfo_height()))
  url = entry_url.get()
  try:
    video = pafy.new(url)
  except ValueError:
    messagebox.showinfo("Error", "Not a valid youtube URL.")
    return
  
  label_url.destroy()
  entry_url.destroy()
  button_run.destroy()

  label_downloading = Label(root, text="Please wait, downloading...")
  label_downloading.grid(padx=padding, pady=padding)
  root.update()

  path = os.path.dirname(os.path.realpath(__file__)) + "\\"
  if mac: path = os.path.dirname(os.path.realpath(__file__)) + "/"
  
  title = video.title
  if title.startswith(" ") or title.startswith("0"): title = "_" + title
  for newChar in[["_", ["<", ">", "/", "\\", "*"]], ["-", [":", '"']], ["", ["?"]]]:
    for forbidenChar in newChar[1]:
      title = title.replace(forbidenChar, newChar[0])
  
  video = pafy.new(url)
  bestaudio = video.audiostreams
  bestaudio.reverse()

  found = False
  for a in bestaudio:
    if not a.extension == "webm":
      bestaudio = a
      found = True
      break

  if not found: bestaudio = video.getbestaudio()

  try:
    bestaudio.download(path+title+ "." + bestaudio.extension)
    label_downloading.destroy()
    Label(root, text="Download complete (."+bestaudio.extension+")").grid(padx=padding, pady=padding)
  except:
    label_downloading.destroy()
    Label(root, text="Download failed. File with that name already exists.").grid(padx=padding, pady=padding)
  root.update()

label_url = Label(root, text="URL: ")
label_url.grid(row=0, column=0, sticky="E", padx=(padding, 0), pady=(padding, 0))

entry_url = Entry(root, width=50)
entry_url.grid(row=0, column=1, padx=(0, padding), pady=(padding, 0))
entry_url.bind("<Return>", keybind)

button_run = Button(root, text="Download", command=run)
button_run.grid(row=1, column=0, columnspan=2, sticky="EW", padx=padding, pady=(0, padding))

root.mainloop()
