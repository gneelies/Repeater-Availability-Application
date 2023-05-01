
# Import modules
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import pytz
import requests


software_version = 'v1.1'
IST = pytz.timezone('America/New_York')


app = Tk()

# App Geometry and components
app.geometry("700x480+600+300")
app.title(f"Repeater Availability Checker  {software_version}")
app.iconbitmap("Images_Icons\local_repeater.ico")
app.resizable(False, True)
app.config(background = '#293241')

## DEFAULT values
STATE = 'Massachusetts'

# Color value reference
top_left_frame_bg  = "#5c4ce1"
top_right_frame_bg = '#867ae9'

# Frame details
frame1 = Frame(app, height = 120, width=180, bg= top_left_frame_bg, bd=1, relief = FLAT)
frame1.place(x=0,y=0)

frame2 = Frame(app, height = 120, width=520, bg= top_right_frame_bg, bd=1, relief = FLAT)
frame2.place(x=180,y=0)

frame3 = Frame(app, height = 30, width=700, bg= 'black', bd=1, relief = RAISED)
frame3.place(x=0,y=120)

# Labels
label_date_now = Label(text="Current Date", bg = top_left_frame_bg, font = 'Verdana 12 bold')
label_date_now.place(x=20, y=40)

label_time_now = Label(text="Current Time", bg = top_left_frame_bg, font = 'Verdana 12')
label_time_now.place(x=20, y=60)

label_location = Label(text="Location", bg = top_right_frame_bg, font = 'Verdana 11')
label_location.place(x=220, y=15)

label_search_repeat = Label(text="Search \nAvailable Repeater", bg = top_right_frame_bg, font = 'Verdana 8')
label_search_repeat.place(x=570, y=70)

label_head_result = Label(text="Callsign   \t    ID  \t      Frequency  \t       Input Frequency \t       Status \t     ", bg = 'black', fg='white', font = 'Verdana 8 bold')
label_head_result.place(x=10, y=125)


# Entry boxes
location_text_var = StringVar()
location_textbox = Entry(app,width = 11, bg = '#eaf2ae', fg= 'black', textvariable = location_text_var, font='verdana 11')
location_textbox['textvariable'] = location_text_var
location_textbox.place(x= 220, y=40)

## TEXT BOX - for RESULTs
result_box_call = Text(app, height = 20, width = 8, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_call.place(x= 12 , y= 152)
result_box_id = Text(app, height = 20, width = 10, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_id.place(x= 125 , y= 152)
result_box_frequency = Text(app, height = 20, width = 15, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_frequency.place(x= 175 , y= 152)
result_box_input = Text(app, height = 20, width = 15, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_input.place(x= 300 , y= 152)
result_box_status = Text(app, height = 20, width = 12, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_status.place(x= 500 , y= 152)


## Defining Functions

# Detect Automatic Location
def fill_location_with_radio():
    curr_location = get_location_ip_service(url)
    location_text_var.set(curr_location)

url = 'https://ipinfo.io/region'
def get_location_ip_service(url):
    response_location = requests.get(url).text
    return response_location

def update_clock():
    raw_TS = datetime.now(IST)
    date_now = raw_TS.strftime("%d %b %Y")
    time_now = raw_TS.strftime("%H:%M:%S %p")
    formatted_now = raw_TS.strftime("%m-%d-%Y")
    label_date_now.config(text = date_now)
    # label_date_now.after(500, update_clock)
    label_time_now.config(text = time_now)
    label_time_now.after(1000, update_clock)
    return formatted_now

def refresh_api_call(STATE):
    headers = {'User-Agent': 'My User Agent 1.0', 'From': 'gneelies@gmail.com'}
    request_link = f"https://www.repeaterbook.com/api/export.php?country=United%20States?state={STATE}"
    response = requests.get(request_link, headers = headers)
    resp_JSON = response.json()['results']
    return resp_JSON

def clear_result_box():
    result_box_call.delete('1.0', END)
    result_box_id.delete('1.0', END)
    result_box_frequency.delete('1.0', END)
    result_box_input.delete('1.0', END)
    result_box_status.delete('1.0', END)

def search_repeater_avl():
    clear_result_box()
    STATE = location_text_var.get().strip()
    resp_JSON = refresh_api_call(STATE)

    try:
        if len(resp_JSON) == 0:
            messagebox.showinfo("INFO","Repeater not available for given date")

        for info in resp_JSON:
            call            = info['Callsign']
            id              = info['Rptr ID']
            frequency       = info['Frequency']
            input           = info['Input Freq']
            status          = info['Operational Status']

            
            '''
            This is not the optimized approach but for the time being I could able to find this alternative solution.
            Somehow, the center name is getting aligned but at the same time it is not limiting itself in the specified area
            rather, it disturb the alignment of the next column (age group). Therefore, I have to create separate columns for
            each entity. The issue with this approach is, each column is scrolling separately which is kind of mess while 
            dealing with more rows.
            There is a solution, however, which is to make a frame and make this as root of all the textbox and also create
            a vertical scrollbar fixed to that root frame- that will scroll of of them together.
            '''

            # data_msg = f" {curr_status:<12}{center_name:<35.30}{age_grp:^20}{vaccine_name: ^10}{qnty_dose_1:^5}{qnty_dose_2:^5}\n"
            # data_msg = "{0:<12}{1:<40}{2:<10}{3:<10}{4:<5}{5:<5}\n".format(curr_status,center_name,age_grp,vaccine_name,qnty_dose_1,qnty_dose_2)
            # result_box.insert(END, " {0:<10s} {1:<30.28s}    {2:<10s} {3:<14s}  {4:<5} {5:<5} {6:^8}\n".format(curr_status,center_name,str(age_grp),vaccine_name,str(qnty_dose_1),str(qnty_dose_2), available_capacity))
            # result_box.insert(END, str.rjust(age_grp, 8))
            result_box_call.insert(END, f"{call}")
            result_box_call.insert(END,"\n")
            result_box_id.insert(END, f"{id}")
            result_box_id.insert(END,"\n")
            result_box_frequency.insert(END, f"{frequency}")
            result_box_frequency.insert(END,"\n")
            result_box_input.insert(END, f"{input}")
            result_box_input.insert(END,"\n")
            result_box_status.insert(END, f"{status}")
            result_box_status.insert(END,"\n")
            
    except KeyError as KE:
        messagebox.showerror("ERROR","No Available repeater(s) for the given state")
        print (location_text_var.get())

# Buttons
search_repeater_image = PhotoImage(file= "Images_Icons\search-icon.png")
search_repeater_btn = Button(app, image=search_repeater_image, bg= top_right_frame_bg, command = search_repeater_avl, relief= RAISED)
search_repeater_btn.place(x = 600,y = 25)

# Radio Buttons
curr_loc_var = StringVar()
radio_location = Radiobutton(app, text="Current location", bg= top_right_frame_bg, variable= curr_loc_var, value = curr_loc_var, command = fill_location_with_radio) #state=DISABLED
radio_location.place(x=215, y=65)


update_clock()

app.mainloop()