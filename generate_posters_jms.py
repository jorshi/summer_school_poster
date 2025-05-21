import os
import pandas as pd
from tqdm import tqdm
from textwrap3 import wrap
from reportlab.lib.pagesizes import A2
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from PIL import Image as PILImage
from pypdf import PdfMerger


name_to_visual_filename = {
    "Yannis Vasilakis": "Screenshot from 2024-05-13 16-55-10 - Yannis Vasilakis.png",
    "Jack Loth": "Capture d’écran 2024-05-14 à 10.25.55 - Jack Loth.png",
    "Carey Bunks": "carey_bunks_aim_summer_school - Carey Bunks.png",
    "Luca Marinelli": "Screenshot 2024-05-14 162616 - Luca Marinelli.png",
    "Huan Zhang": "stage_2 - Huan Zhang.png",
    "Bradley Aldous": "image_2024-05-17_101403441 - B A.png",
    "Rodrigo Diaz": "figures-pipeline (1)-1 - Rodrigo Diaz.png",
    "Ruby Crocker": "aro_val-remains - ruby crocker.png",
    "Chin-Yun Yu": "UPF Lightning presentation - Chin-Yun Yu (Joey).png",
    "Xavier Riley": "ss_img - Xavier Riley.png",
    "Keshav Bhandari": "YIN-YANG POSTER - Keshav Bhandari.png",
    "Kasia Adamska": "poster_flowchart_summer_school - Katarzyna Adamska.png",
    "Christos Plachouras": "1000014893 - Christos Plachouras.png",
    "Marco Pasini": "ConsistencyAutoArch - Marco Pasini.png",
    "Adam Garrow": "Summer School poster image - Adam Garrow.png",
    "Franco Caspe": "summer school poster2 - Franco Caspe.png",
    "Dave Foster": "DF Summer School 2024 Poster - Dave Foster.png",
    "Julien Guinot": "SummerSchool.drawio - Julien Guinot.png",
    "Ashley Noel-Hirst": "ismirdiagrams 2 - Ashley Noel-Hirst.png",
    "Ben Hayes": "Picture 1 - Ben Hayes.png",
    "Haokun Tian": "tree - Haokun Tian.jpg",
    "Aditya Bhattacharjee": "poster_summer_school - Aditya Bhattacharjee.png",
    "Farida Yusuf": "aim_ss_img_bg - Farida Yusuf.png",
    "Yinghao Ma": "WechatIMG2931 - 寒风热血.jpg",
    "Yazhou Li": "poster - Yazhou Li.png",
    "David Südholt": "summer school poster - David Südholt.png",
    "Christopher Mitcheltree": "synth - Christopher Mitcheltree.png",
    "Qiaoxi Zhang": "poster - Josie N.png",
    "Carlos De La Vega Martin": "1000009468 - A A.png",
    "Soumya Sai Vanka": "Music Mixing Technical and creative considerations Highly context-dependent (3) - Sai Soumya.png",
    "James Bolt": "methodology - James Bolt.png",
    "Yin-Jyun Luo": "Screenshot 2024-05-22 at 13.13.05 - Yin-Jyun Luo.png",
    "Corey Ford": "Screenshot 2024-05-22 at 13.58.03 - Corey Ford.png",
    "Shuoyang Zheng": "interface_2 - Jasper Zheng.jpg",
    "Yifan Xie": "poster_figure - yifan xie.png",
    "Ningzhi Wang": "CoordVAE - Ningzhi Wang.png",
    "Yixiao Zhang": "Snipaste_2024-05-23_02-07-16 - Yixiao Zhang (Peanuts).png",
    "Alexander Williams": "summer_school - Alex Williams.png",
    "Jordie Shier": "timbre_remap - Jordie Shier.png",
    "Harnick Khera": "ch8_model - Harnick Khera.png",
    "Sara Cardinale": "Screenshot from 2024-05-23 14-56-07 - Sara Cardinale.png",
    "Xiaowan Yi": "xyi-kong-sequencer - xiaowan.png",
    "Zixun Guo": "Screenshot 2024-05-27 at 11.46.42 - Nicolas guo.png",
    "Qing Wang": "music2dance_generation - Apple Wang.png",
}


def visual_find_person(
    student_name, visuals_path
):  # TO DO, not suitable for every case, double check, name surname etc., once match student names to file names, here bulky
    file_names = os.listdir(visuals_path)
    matched_index = [
        index
        for index, file_name in enumerate(file_names)
        if student_name in file_name and file_name[-4:] != ".pdf"
    ]  # more than 1?, TO DO automatic pdf to png converter
    return file_names[matched_index[0]]


def text_wrapper(
    canvas,
    text,
    wrapper_width=40,
    text_origin=(200, 1200),
    font_type="Helvetica",
    font_size=30,
    centered=False,
    page_width=None,
):
    text_lines = wrap(text, wrapper_width)
    max_line_width = max(
        [stringWidth(line, font_type, font_size) for line in text_lines]
    )
    wraped_text = "\n".join(text_lines)

    if centered:
        assert page_width is not None  # must supply page width if centered
        x = (page_width - max_line_width) / 2.0
        y = text_origin[1]
    else:
        x = text_origin[0]
        y = text_origin[1]

    text_object = canvas.beginText()
    text_object.setTextOrigin(x, y)
    text_object.setFont(font_type, font_size)
    text_object.textLines(wraped_text)
    canvas.drawText(text_object)


def new_text_wrapper(
    canvas,
    text,
    wrapper_width=40,
    text_origin=(200, 1200),
    font_type="Helvetica",
    font_size=30,
    centered=False,
):
    canvas.setFont(font_type, font_size)
    wraped_text = "\n".join(wrap(text, wrapper_width))
    print(wraped_text)
    canvas.drawCentredString(text_origin[0], text_origin[1], wraped_text)


def generate_poster(
    output_dir: str,
    student_name: str,
    cohort: str,
    supervisor_name: str,
    project_title: str,
    answered_question: str,
    unanswered_question: str,
    visual_path: str,
):
    filepath = output_dir + student_name + "_Poster.pdf"
    canvas = Canvas(filepath, pagesize=A2)
    page_width = A2[0]
    page_height = A2[1]

    # AIM Logo
    image_filepath = "Logos/AIM_logo.png"
    img = PILImage.open(image_filepath)
    width, height = img.size
    logo_height = 40
    factor = logo_height / height
    width *= factor
    height *= factor

    x = 125
    y = 1580

    canvas.drawImage(
        image_filepath,
        x,
        y,
        width=width,
        height=height,
        preserveAspectRatio=False,
    )

    # AIM title
    text_wrapper(
        canvas,
        "AIM Summer School 2024",
        40,
        (125 + 15 + width, 1590),
        "Helvetica",
        24,
        centered=False,
        page_width=page_width,
    )

    # precompute number of lines in title
    title_wrap_width = 40
    num_text_lines = len(wrap(project_title, title_wrap_width))

    # title
    text_wrapper(
        canvas,
        project_title,
        40,
        (100, 1500),
        "Helvetica-Bold",
        48,
        centered=True,
        page_width=page_width,
    )
    title_end = 1500 - (num_text_lines * 48)

    # student name
    text_wrapper(
        canvas,
        student_name,
        40,
        (100, title_end - 35),
        "Helvetica",
        32,
        centered=True,
        page_width=page_width,
    )

    # student cohort
    text_wrapper(
        canvas,
        cohort,
        40,
        (100, title_end - 70),
        "Helvetica",
        24,
        centered=True,
        page_width=page_width,
    )

    canvas.setFont("Helvetica", 30)

    # canvas.drawString(200, 1100, supervisor_name)

    image_filepath = os.path.join(visual_path, name_to_visual_filename[student_name])
    img = PILImage.open(image_filepath)
    width, height = img.size

    max_img_width = 750
    factor = max_img_width / width
    width1 = width * factor
    height1 = height * factor

    max_img_height = 500
    factor = max_img_height / height
    width2 = width * factor
    height2 = height * factor

    if height1 > max_img_height:  # use width2
        width = width2
        height = height2
    elif width2 > max_img_width:
        width = width1
        height = height1

    x = (page_width - width) / 2
    y = 1260 - height

    canvas.drawImage(
        image_filepath,
        x,
        y,
        width=width,
        height=height,
        preserveAspectRatio=False,
        mask="auto",
    )

    # precompute number of lines in answered question
    answered_question_wrap_width = 60
    num_text_lines = len(wrap(answered_question, answered_question_wrap_width))

    wrap_width = 65

    text_wrapper(
        canvas,
        "Finding",
        60,
        (175, y - 100),
        "Helvetica-Bold",
        36,
    )

    # answered question
    text_wrapper(
        canvas,
        answered_question,
        wrap_width,
        (175, y - 140),
        "Helvetica",
        28,
    )
    answered_question_end = y - 130 - (num_text_lines * 30)

    text_wrapper(
        canvas,
        "Question",
        60,
        (175, answered_question_end - 100),
        "Helvetica-Bold",
        36,
    )

    # unanswered question
    text_wrapper(
        canvas,
        unanswered_question,
        wrap_width,
        (175, answered_question_end - 140),
        "Helvetica",
        28,
    )

    text_wrapper(
        canvas,
        f"Supervisor(s): {supervisor_name}",
        300,
        (175, 65),
        "Helvetica",
        22,
    )

    canvas.save()


if __name__ == "__main__":
    # ********************** Parameters to check *************************

    expected_number_of_posters = 44
    csv_file = "2024 AIM Summer School Posters.csv"  # csv file name, assuming that it's in the same folder
    visuals_folder = "./Visuals_2024/"
    output_dir = "./Posters_2024/"
    merge_pdfs = True

    # *******************************************************************

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.read_csv(csv_file)

    # Has the questions as the labels, the following indices hard coded

    student_names = df.iloc[:, 1]
    supervisor_names = df.iloc[:, 2]
    cohorts = df.iloc[:, 3]
    project_titles = df.iloc[:, 4]
    answered_questions = df.iloc[:, 6]
    unanswered_questions = df.iloc[:, 7]
    papers = df.iloc[:, 8]

    print(len(student_names))
    assert (
        len(student_names) == expected_number_of_posters
    ), "Expected number of students doesn't match the csv file."

    for student_index in tqdm(range(expected_number_of_posters)):
        generate_poster(
            output_dir,
            student_names[student_index],
            str(cohorts[student_index]),
            supervisor_names[student_index],
            project_titles[student_index],
            answered_questions[student_index],
            unanswered_questions[student_index],
            visuals_folder,
        )

    if merge_pdfs:
        pdf_merger = PdfMerger()
        for filename in os.listdir(output_dir):
            if filename.endswith(".pdf") and "All" not in filename:
                pdf_merger.append(os.path.join(output_dir, filename))
        pdf_merger.write(os.path.join("All_Posters.pdf"))
        pdf_merger.close()
