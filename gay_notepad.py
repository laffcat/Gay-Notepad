import tkinter as tk
import tkinter.font as font
from tkinter.filedialog import askopenfilename, asksaveasfilename





####     🗹 CONFIG     ####    if you wanna tweak some stuff w/o digging thru code

FONT = "Arial"
FONT_SIZE = 13

WINDOW_BG = "Black" # color for text display background. use HTML color names or hex codes (with the #)
POPUP_COLOR = "DarkMagenta" # to control how badly u get flashbanged by the unsaved changes dialogue
POPUP_TEXT_COLOR = "LightSalmon"

COLOR_CYCLE_AMT = 4 # -360 to 360. amount of hue shift per keypress
# 🚨 flashing lights warning if you turn this up too high! 🚨
COLOR_SATURATION = 80 # 0 to 100
COLOR_LIGHTNESS = 90 # 0 to 100

SHADE_SHIFT_HUE = 33 #  -360 to 360. added to hue of darker color shades
SHADE_SAT = 26
SHADE_SAT2 = 17
SHADE_LIGHT = 27
SHADE_LIGHT2 = 9

WINDOW_TITLE = "✨  GAY NOTEPAD  ✨"







####   👩‍💻



####   COLOR MATH - code taken from: www.jameslmilner.com/posts/converting-rgb-hex-hsl-colors/
#                   converted from TypeScript to Python by GPT

def h2x(hsl): # HSL to hex
    h, s, l = hsl['h'], hsl['s'], hsl['l']

    h_decimal = l / 100
    a = (s * min(h_decimal, 1 - h_decimal)) / 100

    def f(n):
        k = (n + h / 30) % 12
        color = h_decimal - a * max(min(k - 3, 9 - k, 1), -1)
        return format(round(255 * color), '02x')

    return '#' + f(0) + f(8) + f(4)

def x2h(hex_code): # hex to HSL
    hex_code = hex_code.lstrip('#')
    if len(hex_code) != 6:
        raise ValueError("Invalid Hex Color")

    r_hex, g_hex, b_hex = int(hex_code[0:2], 16), int(hex_code[2:4], 16), int(hex_code[4:6], 16)
    r, g, b = r_hex / 255, g_hex / 255, b_hex / 255

    max_rgb = max(r, g, b)
    min_rgb = min(r, g, b)

    h = (max_rgb + min_rgb) / 2
    s = h
    l = h

    if max_rgb == min_rgb:
        return {'h': 0, 's': 0, 'l': round(l * 100)}

    d = max_rgb - min_rgb
    s = d / (2 - max_rgb - min_rgb) if l > 0.5 else d / (max_rgb + min_rgb)

    if max_rgb == r:
        h = (g - b) / d + (6 if g < b else 0)
    elif max_rgb == g:
        h = (b - r) / d + 2
    elif max_rgb == b:
        h = (r - g) / d + 4

    h /= 6
    h = round(360 * h)
    s = round(s * 100)
    l = round(l * 100)

    return {'h': h, 's': s, 'l': l}



# storage vars
color_x = "#FFB6C1"
color_h = x2h(color_x)
color_h["s"] = COLOR_SATURATION
color_h["l"] = COLOR_LIGHTNESS
color_x = h2x(color_h)
events = []


######  GENERAL LOGIC

def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Gay Text Files", "*.txt"), ("All Gay Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"{WINDOW_TITLE} - {filepath}")

def save_file():
    """Save the current file as a new one."""
    filepath = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("💖   Gay Text Files   🌈", ".txt"), 
            ("💃   All Gay Files   💅", "*.*")
    ])
    if not filepath:
        return
    with open(filepath, mode="w", encoding="utf-8") as output_file:
        text = txt_edit.get("1.0", tk.END)
        output_file.write(text)
    window.title(f"{WINDOW_TITLE} = {filepath}")
    
    #messagebox.showinfo("Saved", "Changes saved successfully")
    global unsaved_changes
    unsaved_changes = False

    try: 
        shpee.destroy()
        window.destroy()
    except NameError: 
        print(f"Saved {filepath}")
        pass

def on_close():
    if unsaved_changes:
        custom_message_box = tk.Toplevel(window, bg=POPUP_COLOR, pady=9)
        custom_message_box.title("🚨  Unsaved Gay Changes!!!  😱")
        
        global shpee
        shpee = custom_message_box
        
        # Set minimum size
        custom_message_box.minsize(120, 160)  # Set the minimum width to 120 pixels
        custom_message_box.resizable(width=False,height=False)
        
        # Remove minimize and maximize buttons
        custom_message_box.attributes("-toolwindow", 1)  # Removes minimize and maximize buttons
        
        label = tk.Label(
            custom_message_box, text="°º🌺ø,¸,ø🌺º°`°º🌺ø,¸,ø🌺º°`°º🌺ø,¸,ø🌺º°`°º🌺ø,¸,ø🌺º°`°º🌺ø,\n\n🌼    Do you want to save gay changes before closing?    🌻\n\n¸,ø💮º°`°º💮ø,¸,ø💮º°`°º💮ø,¸,ø💮º°`°º💮ø,¸,ø💮º°`°º💮ø,¸,ø💮º°", 
            bg=POPUP_COLOR, fg=POPUP_TEXT_COLOR#, font=("Helvetica", 12)
        )
        label.pack(padx=20, pady=10)
        
        button_save = tk.Button(custom_message_box, text="Save", command=save_file, bg=POPUP_COLOR, fg=POPUP_TEXT_COLOR)
        button_save.place(x=68, y=105)
        
        button_discard = tk.Button(custom_message_box, text="Discard", command=window.destroy, bg=POPUP_COLOR, fg=POPUP_TEXT_COLOR)
        button_discard.place(x=146, y=112)
        
        button_cancel = tk.Button(custom_message_box, text="Cancel", command=custom_message_box.destroy, bg=POPUP_COLOR, fg=POPUP_TEXT_COLOR)
        button_cancel.place(x=238, y=105)
    else:
        window.destroy()  # No unsaved changes, close the program





######      COLOR CYCLING (keypress event)
        
def handle_keypress(_event):    

# Any keypress counts as an unsaved change, even if it didnt actually change anything lmao
    global unsaved_changes
    #if unsaved_changes is False:
    unsaved_changes = True
        #window.title(window.title() + "*")

# Cycle hue, create first color
    color_h["h"] += COLOR_CYCLE_AMT
    color_h["h"] %= 360
    # Apply
    color_x = h2x(color_h)
    txt_edit.configure(fg=color_x)  
    btn_open.configure(fg=color_x)
    btn_save.configure(fg=color_x)
    #btn_opt.configure(fg=color_x)

# Inverted color, mainly for selection highlights
    clr_inv_h = {
        "h":(color_h["h"]+180)%360, 
        "s":COLOR_SATURATION, 
        "l":COLOR_LIGHTNESS
    }
    clr_inv_x = h2x(clr_inv_h)
    # Apply
    txt_edit.configure(selectforeground=clr_inv_x)

# Shading lv1
    clr_bg_h = {
        "h":(color_h["h"]+SHADE_SHIFT_HUE)%360, 
        "s":SHADE_SAT, 
        "l":SHADE_LIGHT
    }
    clr_bg_x = h2x(clr_bg_h)
    # Apply
    btn_open.configure(bg=clr_bg_x)
    btn_save.configure(bg=clr_bg_x)
    txt_edit.configure(insertbackground=clr_bg_x)  
    #btn_opt.configure(bg=clr_bg)

# Shading lv2
    clr_bg_h = {
        "h":(clr_bg_h["h"]+SHADE_SHIFT_HUE)%360, 
        "s":SHADE_SAT2, 
        "l":SHADE_LIGHT2
    }
    clr_bg_x = h2x(clr_bg_h)
    # Apply
    frm_buttons.configure(bg=clr_bg_x)
    txt_edit.configure(selectbackground=clr_bg_x)





###########  Tthe real shit :3

window = tk.Tk()
window.title(WINDOW_TITLE)

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=50, weight=1)

txt_edit = tk.Text(
    window, bg=WINDOW_BG, fg=color_x, 
    blockcursor=True, insertbackground=color_x, 
    insertunfocussed="solid", 
    spacing1=3, padx=20, pady=16,
    wrap="word",
    font=font.Font(family=FONT, size=FONT_SIZE)
)
frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2, bg="#2a2730", pady=4)
btn_open = tk.Button(frm_buttons, text="Open", command=open_file, bg="#5b4755", fg=color_x)
btn_save = tk.Button(frm_buttons, text="Save As...", command=save_file, bg="#5b4755", fg=color_x)
#btn_opt = tk.Button(frm_buttons, text="Options", command=options, bg="#5b4755", fg=color_x)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=3)
btn_save.grid(row=1, column=0, sticky="ew", padx=5, pady=3)
#btn_opt.grid(row=2, column=0, sticky="ew", padx=5, pady=3)

frm_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

unsaved_changes = False

window.bind("<Key>", handle_keypress)
window.protocol("WM_DELETE_WINDOW", on_close)  # Handle window closing
handle_keypress(True)

window.mainloop()








