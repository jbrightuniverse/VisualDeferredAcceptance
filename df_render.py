import os
os.system("pip install Pillow")
os.system("pip install ipywidgets")

import requests
r = requests.get("https://github.com/jbrightuniverse/VisualDeferredAcceptance/raw/main/OpenSansEmoji.ttf")
with open("OpenSansEmoji.ttf", "wb") as f:
    f.write(r.content)

from base64 import b64encode 
from collections import defaultdict
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def process(img, type = "png"):
    filex = BytesIO()
    if type == "png":
        img.save(filex, "PNG")
        into = "png"
    else:
        img[0].save(fp=filex, format='GIF', append_images=img[1:], save_all=True, duration=type, loop=0)
        into = "gif"
    # display trick derived from https://stackoverflow.com/questions/26649716/how-to-show-pil-image-in-ipython-notebook/32108899#32108899
    return f"<img src='data:image/{into};base64,{b64encode(filex.getvalue()).decode('utf-8')}'/>"

def super_simple_example(school_capacities, students, schools):
    img = Image.new("RGBA", (300, 240), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("OpenSansEmoji.ttf", 10)
    for student in range(students):
        draw.ellipse((0, 40 * student, 30, 30 + 40 * student), fill = (18, 137, 222, 255))
        draw.text((13, 40 * student + 11), str(student + 1), font = font)

    for school in range(schools):
        draw.rectangle((150, 12 + 80 * school, 295, 48 + 80 * school), fill = (136, 255, 136, 255))
        draw.text((153, 80 * school + 12), "Program " + str(school + 1), font = font, fill = (0, 0, 0, 255))
        for cap in range(school_capacities[school]):
            draw.rectangle((220 + 40 * cap, 14 + 80 * school, 252 + 40 * cap, 46 + 80 * school), outline = (0, 0, 0, 255))

    return img

def characteristic_example(characteristics, students):
    img = Image.new("RGBA", (700, 240), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("OpenSansEmoji.ttf", 15)
    font2 = ImageFont.truetype("OpenSansEmoji.ttf", 10)
    for student in range(students):
        if student % 2 == 0: height = 10
        else: height = 150
        draw.rectangle((80 * student, height, 135 + 80 * student, height + 80), fill = (18, 137, 222, 255))
        draw.text((80 * student + 5, height), "Student " + str(student + 1), font = font)
        base = 15
        for element in characteristics[student]:
            draw.text((80 * student + 5, height + base), "· " + element, font = font2)
            base += 15
            
    return img
    
def priority_group_example(all_ordered_groups, priority_group_dict, program_data):
    imgs = []
    font = ImageFont.truetype("OpenSansEmoji.ttf", 15)
    font2 = ImageFont.truetype("OpenSansEmoji.ttf", 10)
    for program in program_data:
        img = Image.new("RGBA", (700, 240), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)
        ordered_groups = all_ordered_groups[program]
        priority_groups = priority_group_dict[program]
        for i in range(len(ordered_groups)):
            if i % 2 == 0: height = 10
            else: height = 150
            draw.rectangle((90 * i, height, 158 + 90 * i, height + 80), fill = (200, 255, 200, 255))
            draw.text((90 * i + 5, height), ordered_groups[i] + f" ({i + 1})", font = font, fill = (0, 0, 0, 255))
            if ordered_groups[i] in priority_groups:
                base = 1
                for student in priority_groups[ordered_groups[i]]:
                    draw.ellipse((90 * i + base, height + 25, 90 * i + base + 50, height + 75), fill = (18, 137, 222, 255))
                    draw.text((90*i + base + 1, height + 43), student, font = font2)
                    base += 53
        draw.text((200, 110), program + " Preferences", font = font, fill = (0, 0, 0, 255))
        imgs.append(img)
        
    return imgs

def separator():
    return Image.new("RGBA", (630, 10), (0, 0, 255, 255))

def localized_render_stage(state = None, form = None, program_data = None, pref = None):
    program_preferences = pref
    if not state:
        schools = defaultdict(list)
        working_copy_of_students = {name: {"form": form[name]["form"].copy(), "accepted": False} for name in form}
        upbases = {name: 0 for name in working_copy_of_students}
        leftbases = {name: 0 for name in working_copy_of_students}
        is_matched = defaultdict(lambda: "")
    
    else:
        working_copy_of_students, schools, upbases, leftbases, is_matched = state
    
    student_names = list(working_copy_of_students.keys())
    font = ImageFont.truetype("OpenSansEmoji.ttf", 10)
    font2 = ImageFont.truetype("OpenSansEmoji.ttf", 10)
    font3 = ImageFont.truetype("OpenSansEmoji.ttf", 16)
    match = {}
    for student in working_copy_of_students:
        if len(working_copy_of_students[student]["form"]):
            match[student] = working_copy_of_students[student]["form"][0]

    o_ellipsecol = [18, 137, 222, 255]
    o_prefcol = [136, 255, 136, 255]
    o_textcol = [0, 0, 0, 255]
    speed = 3
    flag = 0
    imgs = []
    imgs2 = []

    ellipsecol = o_ellipsecol.copy()
    prefcol = o_prefcol.copy()
    textcol = o_textcol.copy()
    ellipsecol2 = o_prefcol.copy() 
    textcol2 = o_textcol.copy()
    counter = 0
    while len(working_copy_of_students[student_names[counter]]["form"]) == 0 or working_copy_of_students[student_names[counter]]["accepted"] == True:
        counter += 1
        if counter == 6:
            return None, working_copy_of_students, schools, upbases, leftbases, is_matched
    select = student_names[counter]
    select2 = ""
    pselect = working_copy_of_students[select]["form"][0]

    fade = 255
    k = 0
    
    ranges = []

    while True:
        img = Image.new("RGBA", (300, 270), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)

        school_names = list(program_data.keys())
        for school_name in program_data:
            school = school_names.index(school_name)
            draw.rectangle((150, 12 + 80 * school, 295, 48 + 80 * school), fill = [tuple(ellipsecol2), tuple(o_prefcol)][school_name == pselect])
            draw.text((153, 80 * school + 12), school_name, font = font, fill = [tuple(textcol2), tuple(o_textcol)][school_name == pselect])
            for cap in range(program_data[school_name]["capacity"]):
                draw.rectangle((220 + 40 * cap, 14 + 80 * school, 252 + 40 * cap, 46 + 80 * school), outline = [tuple(textcol2), tuple(o_textcol)][school_name == pselect])

        for student in range(len(student_names)):
            name = student_names[student]
            if flag == 3 and name == select:
                leftbases[name] += 10
                if leftbases[name] == 220 + 40 * len(schools[pselect]): leftbases[name] += 1
            elif flag == 6 and name == select2:
                leftbases[name] -= 10
                if leftbases[name] == 1: leftbases[name] = 0
            if (flag != 3 or (flag == 3 and (name == select or pselect == is_matched[name]))) or (flag == 6 and name == select2):
                if flag == 3 and name == select:
                    b = 15 + 80 * school_names.index(match[name])
                    a = 40 * student
                    upbases[name] = (b-a) * (min(leftbases[name], 220 + 40 * len(schools[pselect]))/10) // ((220 + 40 * len(schools[pselect]))//10)
                    if b < a and abs(upbases[name] - 16 + 80 * school_names.index(match[name])) <= 2:
                        upbases[name] = 16 + 80 * school_names.index(match[name])
                elif flag == 6 and name == select2:
                    b = 15 + 80 * school_names.index(match[name])
                    a = 40 * student
                    upbases[name] = (b-a) * (min(leftbases[name], 220 + 40 * len(schools[pselect]))/10) // ((220 + 40 * len(schools[pselect]))//10)
                    if b < a and abs(upbases[name] - 40 * student) <= 2:
                        upbases[name] = 40 * student
                draw.ellipse((leftbases[name], upbases[name] + 40 * student, leftbases[name] + 30, upbases[name] + 30 + 40 * student), 
                             fill = [tuple(ellipsecol), tuple(o_ellipsecol)][name == select or name == select2 or (working_copy_of_students[name]["accepted"] and (flag < 2 or pselect == is_matched[name]))])
                draw.text((13 + leftbases[name], upbases[name] + 40 * student + 11), str(student + 1), font = font)

            if flag != 3 and not working_copy_of_students[name]["accepted"]:
                base = 0
                programs = working_copy_of_students[student_names[student]]["form"]
                for program in range(len(programs)):
                    draw.rectangle((40, base + 2 * program + 40 * student, 90, base + 8 + 2 * program + 40 * student), fill = [tuple(prefcol), tuple(o_prefcol)][student_names[student] == select and program == 0])
                    draw.text((41, base + 2 * program - 1 + 40 * student), programs[program], fill = [tuple(textcol), tuple(o_textcol)][student_names[student] == select and program == 0], font = font2)
                    base += 10

        if flag == 4:
            if fade == 1: fade = 0
            thenames = [[a.split(" ")[1], "-"][a not in schools[pselect] + [select]] for a in program_preferences[pselect]]
            draw.text((220, 49 + 80 * school_names.index(pselect)), ", ".join(thenames), fill = (fade, fade, fade, 255), font = font2)
            fade = max(0, fade//2)
        elif flag == 5:
            actual_pref = [[a.split(" ")[1], f"({a.split(' ')[1]})"][a == select] for a in program_preferences[pselect] if a in schools[pselect] + [select]]
            draw.text((220, 49 + 80 * school_names.index(pselect)), ", ".join(actual_pref), fill = (0, 0, 0, 255), font = font2)

        ellipsecol = [min(255, i + speed) for i in ellipsecol]
        prefcol = [min(255, i + speed) for i in prefcol]
        textcol = [min(255, i + speed) for i in textcol]
        speed += min(15, speed)

        if flag == 6:
            if leftbases[select2] == 0:
                schools[pselect].remove(select2)
                del working_copy_of_students[select2]["form"][0]
                working_copy_of_students[select2]["accepted"] = False
                is_matched[select2] = ""
                if len(working_copy_of_students[select2]["form"]) == 0:
                    working_copy_of_students[select2]["accepted"] = True
                else:
                    match[select2] = working_copy_of_students[select2]["form"][0]
                draw.text((5, 240), "Step 5: Reject least-preferred student", fill = (0, 0, 0, 255), font = font3)
                imgs.append(img)
                imgs2.append(img)
                ranges.append(len(imgs))
                for i in range(15):
                    imgs2.append(imgs2[-1])
                flag = 3
            else:
                imgs.append(img)
                imgs2.append(img)

        elif flag == 5:
            student_list = [a for a in program_preferences[pselect] if a in schools[pselect] + [select]]
            if student_list[-1] == select:
                draw.text((5, 240), "Cap Step: No, reject/ignore them", fill = (0, 0, 0, 255), font = font3)
                del working_copy_of_students[select]["form"][0]
                if len(working_copy_of_students[select]["form"]) == 0:
                    working_copy_of_students[select]["accepted"] = True
                    is_matched[select] = ""
                imgs.append(img)
                imgs2.append(img)
                ranges.append(len(imgs))
                for i in range(15):
                    imgs2.append(imgs2[-1])
                if counter != 5:
                    flag = 0
                    counter += 1
                    while len(working_copy_of_students[student_names[counter]]["form"]) == 0 or working_copy_of_students[student_names[counter]]["accepted"] == True:
                        counter += 1
                        if counter == 6:
                            break
                    if counter == 6:
                        break
                    speed = 3
                    k = 0
                    ellipsecol = o_ellipsecol.copy()
                    prefcol = o_prefcol.copy()
                    textcol = o_textcol.copy()
                    ellipsecol2 = o_prefcol.copy() 
                    textcol2 = o_textcol.copy()
                    select = student_names[counter]
                    pselect = working_copy_of_students[select]["form"][0]
                    match[select] = pselect
                else:
                    break
            else:
                draw.text((5, 240), "Step 4: Yes", fill = (0, 0, 0, 255), font = font3)
                imgs.append(img)
                imgs2.append(img)
                ranges.append(len(imgs))
                for i in range(15):
                    imgs2.append(imgs2[-1])
                flag = 6
                select2 = [a for a in program_preferences[pselect] if a in schools[pselect] + [select]][-1]

        elif flag == 4:
            if fade == 0:
                fade = 255
                draw.text((5, 240), "Step 3: Are they better than anyone?", fill = (0, 0, 0, 255), font = font3)
                imgs.append(img)
                imgs2.append(img)
                ranges.append(len(imgs))
                for i in range(15):
                    imgs2.append(imgs2[-1])
                flag = 5
            else:
                imgs.append(img)

        elif flag == 3:
            if leftbases[select] == 221 + 40 * len(schools[pselect]):
                draw.text((5, 240), "Cap Step: Mark student as assigned", fill = (0, 0, 0, 255), font = font3)
                imgs.append(img)
                imgs2.append(img)
                ranges.append(len(imgs))
                for i in range(15):
                    imgs2.append(imgs2[-1])

                schools[pselect].append(select)
                working_copy_of_students[select]["accepted"] = True
                is_matched[select] = pselect
                if counter != 5:
                    flag = 0
                    counter += 1
                    while len(working_copy_of_students[student_names[counter]]["form"]) == 0 or working_copy_of_students[student_names[counter]]["accepted"] == True:
                        counter += 1
                        if counter == 6:
                            break
                    if counter == 6:
                        break
                    speed = 3
                    k = 0
                    ellipsecol = o_ellipsecol.copy()
                    prefcol = o_prefcol.copy()
                    textcol = o_textcol.copy()
                    ellipsecol2 = o_prefcol.copy() 
                    textcol2 = o_textcol.copy()
                    select = student_names[counter]
                    pselect = working_copy_of_students[select]["form"][0]
                else:
                    break

            else:
                imgs.append(img)
                imgs2.append(img)

        elif flag == 2:
            if sum(ellipsecol2 + textcol2) == 255 * 4 * 2:
                if len(schools[pselect]) < program_data[pselect]["capacity"]:
                    draw.text((5, 240), "Step 2: School has space; add student.", fill = (0, 0, 0, 255), font = font3)
                    flag = 3
                else:
                    draw.text((5, 240), "Step 2: School full; find preferences", fill = (0, 0, 0, 255), font = font3)
                    flag = 4
                imgs.append(img)
                imgs2.append(img)
                ranges.append(len(imgs))
                for i in range(15):
                    imgs2.append(imgs2[-1])
            else:
                imgs.append(img)
                imgs2.append(img)
                ellipsecol2 = [min(255, i + speed) for i in ellipsecol2]
                textcol2 = [min(255, i + speed) for i in textcol2]
                speed += min(15, speed - 1)


        elif flag == 1: 
            draw.text((5, 240), "Step 1: Select next student's first choice", fill = (0, 0, 0, 255), font = font3)
            imgs.append(img)
            imgs2.append(img)
            ranges.append(len(imgs))
            for i in range(15):
                imgs2.append(imgs2[-1])
            speed = 5
            flag = 2

        elif sum(ellipsecol + prefcol + textcol) == 255 * 4 * 3 and flag == 0: 
            flag = 1
            imgs.append(img)
            imgs2.append(img)

        else:
            imgs.append(img)
            imgs2.append(img)
            if k == 0:
                k = 1
                for i in range(15):
                    imgs2.append(img)
                    
    return imgs, imgs2, ranges, working_copy_of_students, schools, upbases, leftbases, is_matched


LARGE_RENDER_PROCESS_ONE = """
previous_slide = widgets.Button(description="Previous Step")
replay = widgets.Button(description="Replay Step")
next_slide = widgets.Button(description="Next Step")
speedslide = widgets.FloatSlider(value=0.05, min=0.01, max=0.3, step=0.005)

output = widgets.Output()
outputmid = widgets.Output()
output2 = widgets.Output()
outputslide = widgets.Output()
counter = 0
upgraded_ranges = [0] + [i-1 for i in ranges] + [len(imgs) - 1]
display(previous_slide, output)
display(replay, outputmid)
display(next_slide, output2)
display(widgets.Label(value="Change Render Speed:"))
display(speedslide, outputslide)
with output2:
    display(HTML(process(imgs[0])))

speed = 0.05
    
def prev_callback(b):
    global counter, speed
    with output2:
        if counter > 0:
            counter -= 1
            for i in range(upgraded_ranges[counter - 1], upgraded_ranges[counter] + 1):
                clear_output(wait=True)
                display(HTML(process(imgs[i])))
                time.sleep(speed)
        else:
            counter = 0
            clear_output(wait=True)
            display(HTML(process(imgs[0])))
            
def replay_callback(b):
    global counter, speed
    with output2:
        if counter != 0:
            for i in range(upgraded_ranges[counter - 1], upgraded_ranges[counter] + 1):
                clear_output(wait=True)
                display(HTML(process(imgs[i])))
                time.sleep(speed)
            
def next_callback(b):
    global counter, speed
    with output2:
        if counter < len(upgraded_ranges) - 1:
            counter += 1
            for i in range(upgraded_ranges[counter - 1], upgraded_ranges[counter] + 1):
                clear_output(wait=True)
                display(HTML(process(imgs[i])))
                time.sleep(speed)

def speed_callback(s):
    with output2:
        global speed
        if not isinstance(s["new"], dict):
            speed = s["new"]
            
            
previous_slide.on_click(prev_callback)
replay.on_click(replay_callback)
next_slide.on_click(next_callback)
speedslide.observe(speed_callback)
"""

LARGE_RENDER_PROCESS_TWO = """
previous_slide2 = widgets.Button(description="Previous Step")
replay2 = widgets.Button(description="Replay Step")
next_slide2 = widgets.Button(description="Next Step")
speedslide2 = widgets.FloatSlider(value=0.05, min=0.01, max=0.3, step=0.005)

koutput = widgets.Output()
koutputmid = widgets.Output()
koutput2 = widgets.Output()
koutputslide = widgets.Output()
kcounter = 0
kupgraded_ranges = [0] + [i-1 for i in ranges2] + [len(imgs2) - 1]
display(previous_slide2, koutput)
display(replay2, koutputmid)
display(next_slide2, koutput2)
display(widgets.Label(value="Change Render Speed:"))
display(speedslide2, koutputslide)
with koutput2:
    display(HTML(process(imgs2[0])))

kspeed = 0.05
    
def prev_callback2(b):
    global kcounter, kspeed
    with koutput2:
        if kcounter > 1:
            kcounter -= 1
            for i in range(kupgraded_ranges[kcounter - 1], kupgraded_ranges[kcounter] + 1):
                clear_output(wait=True)
                display(HTML(process(imgs2[i])))
                time.sleep(kspeed)
        else:
            kcounter = 0
            clear_output(wait=True)
            display(HTML(process(imgs2[0])))
            
def replay_callback2(b):
    global kcounter, kspeed
    with koutput2:
        if kcounter != 0:
            for i in range(kupgraded_ranges[kcounter - 1], kupgraded_ranges[kcounter] + 1):
                clear_output(wait=True)
                display(HTML(process(imgs2[i])))
                time.sleep(kspeed)
            
def next_callback2(b):
    global kcounter, kspeed
    with koutput2:
        if kcounter < len(kupgraded_ranges) - 1:
            kcounter += 1
            for i in range(kupgraded_ranges[kcounter - 1], kupgraded_ranges[kcounter] + 1):
                clear_output(wait=True)
                display(HTML(process(imgs2[i])))
                time.sleep(kspeed)

def speed_callback2(s):
    with koutput2:
        global kspeed
        if not isinstance(s["new"], dict):
            kspeed = s["new"]         
            
previous_slide2.on_click(prev_callback2)
replay2.on_click(replay_callback2)
next_slide2.on_click(next_callback2)
speedslide2.observe(speed_callback2)
"""
            
            
LARGE_RENDER_PROCESS_THREE = """
previous_slide3 = widgets.Button(description="Previous Step")
replay3 = widgets.Button(description="Replay Step")
next_slide3 = widgets.Button(description="Next Step")
speedslide3 = widgets.FloatSlider(value=0.05, min=0.01, max=0.3, step=0.005)

k2output = widgets.Output()
k2outputmid = widgets.Output()
k2output2 = widgets.Output()
k2outputslide = widgets.Output()
k2counter = 0
k2upgraded_ranges = [0] + [i-1 for i in ranges3] + [len(imgs3) - 1]
display(previous_slide3, k2output)
display(replay3, k2outputmid)
display(next_slide3, k2output2)
display(widgets.Label(value="Change Render Speed:"))
display(speedslide3, k2outputslide)
with k2output2:
    display(HTML(process(imgs3[0])))

k2speed = 0.05
    
def prev_callback3(b):
    global k2counter, k2speed
    with k2output2:
        if k2counter > 1:
            k2counter -= 1
            for i in range(k2upgraded_ranges[k2counter - 1], k2upgraded_ranges[k2counter] + 1):
                clear_output(wait=True)
                display(HTML(process(imgs3[i])))
                time.sleep(k2speed)
        else:
            k2counter = 0
            clear_output(wait=True)
            display(HTML(process(imgs3[0])))
            
def replay_callback3(b):
    global k2counter, k2speed
    with k2output2:
        if k2counter != 0:
            for i in range(kupgraded_ranges[k2counter - 1], kupgraded_ranges[k2counter] + 1):
                clear_output(wait=True)
                display(HTML(process(imgs3[i])))
                time.sleep(k2speed)
            
def next_callback3(b):
    global k2counter, k2speed
    with k2output2:
        if k2counter < len(k2upgraded_ranges) - 1:
            k2counter += 1
            for i in range(k2upgraded_ranges[k2counter - 1], k2upgraded_ranges[k2counter] + 1):
                clear_output(wait=True)
                display(HTML(process(imgs3[i])))
                time.sleep(k2speed)

def speed_callback3(s):
    with k2output2:
        global k2speed
        if not isinstance(s["new"], dict):
            k2speed = s["new"]         
            
previous_slide3.on_click(prev_callback3)
replay3.on_click(replay_callback3)
next_slide3.on_click(next_callback3)
speedslide3.observe(speed_callback3)
"""