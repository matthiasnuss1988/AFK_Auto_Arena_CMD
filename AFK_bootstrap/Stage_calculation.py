def return_valid_level(rec_level, latest_level, level_not_found=[False]): 
      # Helper function to parse input values and handle reconstruction based on the other input
    def handle_input_errors(value1, value2, ocr_error_msg, sql_error_msg):
        if str(value1).isdigit():
            if str(value2).isdigit():
                return int(value1), int(value2)
            else:
                print(sql_error_msg)
                return int(value1), int(value1)
        else:
            #level_not_found[0] = True
            if str(value2).isdigit():
                print(ocr_error_msg)
                return int(value2), int(value2)
            else:
                print("OCR error and SQL-database: Invalid value for both inputs")
                return 1, 1
    if rec_level == "" or rec_level is None:
        level_not_found[0] = True

    rec_level_int, latest_level_int= handle_input_errors(
        rec_level, latest_level,
        "OCR error: rec_level is reconstructed based on latest_level",
        "SQL-database: latest_level is reconstructed based on rec_level"
    ) 
    if rec_level_int == latest_level_int or latest_level_int <= rec_level_int <= latest_level_int + 5:
        return_value= rec_level_int
    elif level_not_found[0] and rec_level_int >= latest_level_int + 1:
        return_value= rec_level_int
        level_not_found[0] = False
    else:
        return_value=latest_level_int

    return return_value

def return_if_missing(latest_chapter_int, latest_level_int, rec_chapter_int, rec_level_int, len_latest_chapter_range, level_not_found):
    if rec_chapter_int == latest_chapter_int:
        if rec_level_int == latest_level_int or latest_level_int <= rec_level_int <= latest_level_int + 5:
            valid_stage = f"{latest_chapter_int}-{rec_level_int}"
        elif rec_level_int > latest_level_int + 1 and level_not_found[0]:
            valid_stage = f"{latest_chapter_int}-{rec_level_int}"
            level_not_found[0] = False
        else:
            valid_stage = f"{latest_chapter_int}-{latest_level_int}"
    elif rec_chapter_int == latest_chapter_int + 1:
        if rec_level_int == 1 and latest_level_int == len_latest_chapter_range:
            valid_stage = f"{rec_chapter_int}-{rec_level_int}"
        elif rec_level_int > 1 and latest_level_int == len_latest_chapter_range and level_not_found[0]:
            valid_stage = f"{rec_chapter_int}-{rec_level_int}"
            level_not_found[0] = False
        elif rec_level_int == latest_level_int + 1:
            valid_stage = f"{rec_chapter_int}-{rec_level_int}"
        elif latest_level_int < len_latest_chapter_range and rec_level_int:
            valid_stage = f"{rec_chapter_int}-{rec_level_int}"
        else:
            valid_stage = f"{latest_chapter_int}-{latest_level_int}"
    elif rec_chapter_int > latest_chapter_int + 1:
        if rec_level_int and level_not_found[0]:
            valid_stage = f"{rec_chapter_int}-{rec_level_int}"
            level_not_found[0] = False
        else:
            valid_stage = f"{latest_chapter_int}-{latest_level_int}"
    else:
        valid_stage = f"{latest_chapter_int}-{latest_level_int}"
    return valid_stage
       
def return_valid_chapter(rec_chapter, latest_chapter, rec_level, latest_level, level_not_found=[False]):
    chapter_ranges = {
        '1': range(1, 13),
        '2': range(1, 29),
        '3': range(1, 37),
        '4': range(1, 37),
        '5-19': range(1, 41),
        '20-55': range(1, 61)
    }
    # Helper function to parse input values and handle reconstruction based on the other input
    def handle_input_errors(value1, value2, ocr_error_msg, sql_error_msg):
        if str(value1).isdigit():
            if str(value2).isdigit():
                return int(value1), int(value2)
            else:
                print(sql_error_msg)
                return int(value1), int(value1)
        else:
            if str(value2).isdigit():
                print(ocr_error_msg)
                return int(value2), int(value2)
            else:
                print("OCR error and SQL-database: Invalid value for both inputs")
                return 1, 1
    if rec_level == "" or rec_level is None:
        level_not_found[0] = True

    rec_level_int, latest_level_int = handle_input_errors(
        rec_level, latest_level,
        "OCR error: rec_level is reconstructed based on latest_level",
        "SQL-database: latest_level is reconstructed based on rec_level"
    )
    rec_chapter_int, latest_chapter_int = handle_input_errors(
        rec_chapter, latest_chapter,
         "OCR error: rec_chapter is reconstructed based on latest_chapter",
        "SQL-database: latest_chapter is reconstructed based on rec_chapter"
    )
    # Convert the chapter integers to the correct key format (string)
    rec_chapter_key = str(rec_chapter_int) if rec_chapter_int < 5 else '5-19' if rec_chapter_int < 20 else '20-55'
    latest_chapter_key = str(latest_chapter_int) if latest_chapter_int < 5 else '5-19' if latest_chapter_int < 20 else '20-55'
    
    latest_level_in_range = latest_level_int in chapter_ranges[latest_chapter_key]
    len_latest_chapter_range = len(chapter_ranges[latest_chapter_key])
    rec_level_in_range = rec_level_int in chapter_ranges[rec_chapter_key]
    len_rec_chapter_range = len(chapter_ranges[rec_chapter_key])

    
    if latest_level_in_range and rec_level_in_range: 
        valid_stage=return_if_missing(latest_chapter_int, latest_level_int, rec_chapter_int, rec_level_int, len_latest_chapter_range, level_not_found)
    else:
        print("out of range")
        valid_stage = f"-"
    return str(valid_stage)

def return_valid_stage(rec_stage, latest_stage, stage_mode):
    if stage_mode == 1:
        if rec_stage and '-' in rec_stage:
            rec_chapter, rec_level = map(str, rec_stage.split('-'))
        else:
            rec_chapter, rec_level = None, None
            print("OCR error: rec_stage is None or empy")

        if latest_stage and '-' in latest_stage:
            latest_chapter, latest_level = map(str, latest_stage.split('-'))
        else:
            latest_chapter, latest_level = None, None
            print("OCR error: latest_stage is None or empty")
        #if rec_chapter.isdigit() and rec_level.isdigit() and latest_chapter.isdigit() and latest_level.isdigit():
        #print(rec_chapter,latest_chapter, rec_level, latest_level)
        valid_stage = return_valid_chapter(rec_chapter,latest_chapter, rec_level, latest_level)
        #else:
           # print("OCR error: Invalid value for rec_stage or latest_stage")
           # return None

    else:
        #if str(rec_stage).isdigit() and str(latest_stage).isdigit():
        rec_level = rec_stage
        latest_level = latest_stage
        valid_stage = return_valid_level(rec_level, latest_level)
        #else:
        #    print("OCR error: Invalid value for rec_stage or latest_stage")
         #   return None

    
    return str(valid_stage)

# print(return_valid_level("8", "8"))
# print(return_valid_level("", "8"))
# print(return_valid_level("10", "8"))
# print(return_valid_level("12", "10"))
# print(return_valid_level("12", "11"))

# print(return_valid_stage("54-1", None, 1))
# print(return_valid_stage("54-2", "54-1", 1))
# print(return_valid_stage("", "54-2", 1))
# print(return_valid_stage("54-7", "54-2", 1))
# print(return_valid_stage("54-9", "54-7", 1))
# print(return_valid_chapter(54, 54, 2, 1))
# print(return_valid_chapter(54, 54, "", 1))
# print(return_valid_chapter(54, 54, 5, 1))
# print(return_valid_chapter(54, 54, 6, 5))
#print(return_valid_chapter("54",None,"1", None))
#print(return_valid_stage("", "670", 2))
#print(return_valid_stage("673", "670", 2))
#print(return_valid_stage("674", "673", 2))
#print(return_valid_stage("676", "674", 2))

