def valid_start(text):
    if "-" in text:
        start_project = text.split("-")
        return start_project
    else:
        return ("Не правильный формат")

#print(valid_start("ergerg-"))