import datetime
import os

import gantt
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

from core.db import ProjectDB, TaskDB

try:
    import local_settings.config as config
except ModuleNotFoundError:
    import prod_settings.config as config



def generate_diagram(project):
    gantt.define_font_attributes(fill='black',
                             stroke='black',
                             stroke_width=0,
                             font_family="Verdana",)

    gantt.define_not_worked_days([])

    main_project = gantt.Project(name=project.name)

    gantt_performers = []
    gantt_tasks = []

    taskdb = TaskDB(project=project)
    tasks = taskdb.get_all_tasks()
    for task in tasks:
        gantt_task = gantt.Task(
            name=task.name,
            start=task.date_start,
            duration=task.duration
        )
        if task.performers:
            for performer in task.performers:
                gantt_performer = gantt.Project(name=performer.name)
                gantt_performer.add_task(gantt_task)
                gantt_performers.append(gantt_performer)
        else:
            gantt_tasks.append(gantt_task)
                
    [main_project.add_task(task) for task in gantt_tasks]
    [main_project.add_task(task) for task in gantt_performers]

    today_time = datetime.datetime.now()
    today_date = datetime.date(today_time.year, today_time.month, today_time.day)

    main_project.make_svg_for_tasks(filename=os.path.join(config.TMP_PATH, str(project.user)+'.svg'),
                    today=today_date,
                    start=project.date_start,
                    end=project.date_end)
    
    with open(os.path.join(config.TMP_PATH, str(project.user)+'.svg'), 'r') as f:
        svg_string = f.read()

    svg_string = svg_string.replace('lightgray', '#D3D3D3').replace('gray', '#808080').replace('#0000FF ', '#C2C5CC')
    
    with open(os.path.join(config.TMP_PATH, str(project.user)+'.svg'), 'w') as f:
        f.write(svg_string)

    drawing = svg2rlg(os.path.join(config.TMP_PATH, str(project.user)+'.svg'))
    renderPM.drawToFile(drawing, os.path.join(config.TMP_PATH, str(project.user)+'.jpg'), fmt="jpg")
    return os.path.join(config.TMP_PATH, str(project.user)+'.jpg')