import os
import sqlite3
from Stage_calculation import return_valid_stage

def file_path(name):
    dir_path=os.path.dirname(os.path.realpath(__file__))
    path_to_name = os.path.join(dir_path, name)
    return path_to_name

def delete_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' deleted.")
    else:
        print(f"File '{file_path}' not found.")

def create_database_and_table(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stages
                 (id INTEGER PRIMARY KEY, stage_mode TEXT, stage TEXT)''')
    conn.commit()
    conn.close()
    print("Table created")  # Add this line

def is_database_empty(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM stages")
    count = c.fetchone()[0]
    conn.close()
    return count == 0

def get_latest_stage(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("SELECT stage_mode, MAX(id), stage FROM stages GROUP BY stage_mode")
    latest_stage_dict = {row[0]: row[2] for row in c.fetchall()}
    conn.close()
    return latest_stage_dict

def append_stages_to_database(stage_mode, new_stage, database_name):
    try:
        stage_mode_name = get_combat_mode(stage_mode)
        if stage_mode_name.startswith("Invalid"):
            raise ValueError(stage_mode_name)
            
        latest_stage_dict = get_latest_stage(database_name)
        latest_stage = latest_stage_dict.get(stage_mode_name)
        #if latest_stage:
        #print(new_stage,latest_stage,stage_mode)
        valid_stage=return_valid_stage(str(new_stage), str(latest_stage), stage_mode)
        #print(valid_stage)
        #else:
            #  valid_stage=str(new_stage)
        valid_stages = interpolate_stage_update(valid_stage, latest_stage)
        #print(valid_stages)
        if valid_stages:
            conn = sqlite3.connect(database_name)
            c = conn.cursor()

            for stage in valid_stages:
                c.execute("INSERT INTO stages (stage_mode, stage) VALUES (?, ?)", (stage_mode_name, stage))
                print(f"Added stage {stage} to {stage_mode_name}")
            conn.commit()
            conn.close()
        else:
            raise ValueError("No valid stages to add.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def get_combat_mode(number):
    combat_modes = ["Campaign", "King's Tower", "Celestial Sanctum", "Tower of Light", "The Brutal Citadel", "Infernal Fortress", "The Forsaken Necropolis", "The World Tree"]
    try:
        index = int(number) - 1
        if 0 <= index < len(combat_modes):
            return combat_modes[index]
        else:
            raise ValueError("Number out of range.")
    except ValueError:
          return f"Invalid input '{number}'. Please enter a number between 1 and 8."

def initialize_stages(database_name):
    mode_to_number = {
    "Campaign": 1,
    "King's Tower": 2,
    "Celestial Sanctum": 3,
    "Tower of Light": 4,
    "The Brutal Citadel": 5,
    "Infernal Fortress": 6,
    "The Forsaken Necropolis": 7,
    "The World Tree": 8
    }
    if is_database_empty(database_name):
        initial_data = {
            "Campaign": [None],
            "King's Tower": [None],
            "Celestial Sanctum": [None],
            "Tower of Light": [None],
            "The Brutal Citadel": [None],
            "Infernal Fortress": [None],
            "The Forsaken Necropolis": [None],
            "The World Tree": [None]
        }
        for stage_mode, stages in initial_data.items():
            mode_number = mode_to_number[stage_mode]
            for stage in stages:
                append_stages_to_database(mode_number, stage, database_name)

def interpolate_stage_update(valid_stage, latest_stage):
    chapter_ranges = {
        '1': range(1, 13),
        '2': range(1, 29),
        '3-4': range(1, 37),
        '5-19': range(1, 41),
        '20-55': range(1, 61)
    }

    if "-" in valid_stage:
        valid_stage_split = valid_stage.split('-')
        valid_chapter, valid_level = map(int, valid_stage_split)
        if latest_stage:
            latest_stage_split = latest_stage.split('-')
            latest_chapter, latest_level = map(int, latest_stage_split)
        
        rec_chapter_key = str(valid_chapter) if valid_chapter < 5 else '5-19' if valid_chapter < 20 else '20-55'

        all_stages = []
        for chapter_key, chapter_range in chapter_ranges.items():
            for chapter in range(int(chapter_key.split('-')[0]), int(chapter_key.split('-')[-1]) + 1):
                for level in chapter_range:
                    stage = f"{chapter}-{level}"
                    if (latest_stage is None or (int(chapter) > int(latest_chapter) or (int(chapter) == int(latest_chapter) and int(level) > int(latest_level)))) and (int(chapter) < int(valid_chapter) or (int(chapter) == int(valid_chapter) and int(level) <= int(valid_level))):
                        all_stages.append(stage)
    else:
        if latest_stage:
            start_stage = int(latest_stage) + 1
        else:
            start_stage = 1
        end_stage = int(valid_stage)
        all_stages = list(range(start_stage, end_stage + 1))

    return all_stages








# Test the function
#latest_stage = "1-4"
##valid_stage = "5-12"
#print(is_valid_stage_update(latest_stage, valid_stage))

#latest_stage = "5-5"
#valid_stage = "6-12"
#print(is_valid_stage_update(latest_stage, valid_stage))

def view_all_stages(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("SELECT * FROM stages")
    rows = c.fetchall()
    conn.close()

    print("All stages in the database:")
    for row in rows:
        print(f"ID: {row[0]}, Stage Mode: {row[1]}, Stage: {row[2]}")

#database_name = file_path('config.db')
# delete_file(database_name)
# create_database_and_table(database_name)
# initialize_stages(database_name)
# append_stages_to_database(1, "1-3", database_name)
# # append_stages_to_database(1, "1-4", database_name)
# # append_stages_to_database(1, "", database_name)
# # append_stages_to_database(1, "1-7", database_name)
# # append_stages_to_database(1, "", database_name)
# # append_stages_to_database(1, "1-9", database_name)

#view_all_stages(database_name)
# print(get_latest_stage(database_name))
# print(get_latest_stage(database_name).get(get_combat_mode(1)))