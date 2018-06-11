__author__ = 'blazko'
trans_dict = {}
trans_dict[("new_subject","ru")] = "Новая тема"
trans_dict[("new_subject","de")] = "Neues Thema"
trans_dict[("new_subject","en")] = "New subject"


trans_dict[("subjects_list","ru")] = "Редактировать темы"
trans_dict[("subjects_list","de")] = "Themen editieren"
trans_dict[("subjects_list","en")] = "Edit subjects"

trans_dict[("new_exercise","ru")] = "Новое упражнение"
trans_dict[("new_exercise","de")] = "Neue Übung"
trans_dict[("new_exercise","en")] = "New exercise"

trans_dict[("login","ru")] = "Вход"
trans_dict[("login","de")] = "Login"
trans_dict[("login","en")] = "Login"

trans_dict[("logout","ru")] = "Выход"
trans_dict[("logout","de")] = "Logout"
trans_dict[("logout","en")] = "Logout"

trans_dict[("register","ru")] = "Регистрация"
trans_dict[("register","de")] = "Register"
trans_dict[("register","en")] = "Register"

trans_dict[("home_page","ru")] = "Выбрать язык"
trans_dict[("home_page","de")] = "Sprache wählen"
trans_dict[("home_page","en")] = "Select exercise"



trans_dict[("check","ru")] = "Проверить"
trans_dict[("check","de")] = "Prüfen"
trans_dict[("check","en")] = "Check"

trans_dict[("save","ru")] = "Сохранить"
trans_dict[("save","de")] = "Speichern"
trans_dict[("save","en")] = "Save"

trans_dict[("cancel","ru")] = "Отменить"
trans_dict[("cancel","de")] = "Abbrechen"
trans_dict[("cancel","en")] = "Cancel"

trans_dict[("show_results","ru")] = "Результаты упражнения"
trans_dict[("show_results","de")] = "Ergebnisse der Übung"
trans_dict[("show_results","en")] = "Results of exercise"

trans_dict[("play_again","ru")] = "Повторить упражнение"
trans_dict[("play_again","de")] = "Übung viderholen"
trans_dict[("play_again","en")] = "Repeat exercise"

trans_dict[("edit","ru")] = "Редактировать"
trans_dict[("edit","de")] = "Edit"
trans_dict[("edit","en")] = "Edit"

trans_dict[("lang","ru")] = "Русский язык"
trans_dict[("lang","de")] = "Deutsch"
trans_dict[("lang","en")] = "English"

trans_dict[("language_caption","ru")] = "Язык"
trans_dict[("language_caption","de")] = "Sprache"
trans_dict[("language_caption","en")] = "Language"

trans_dict[("subject_caption","ru")] = "Тема"
trans_dict[("subject_caption","de")] = "Thema"
trans_dict[("subject_caption","en")] = "Subject"

trans_dict[("group_caption","ru")] = "Група"
trans_dict[("group_caption","de")] = "Gruppe"
trans_dict[("group_caption","en")] = "Group"

trans_dict[("subjects_list_caption","ru")] = "Список тем"
trans_dict[("subjects_list_caption","de")] = "Themenliste"
trans_dict[("subjects_list_caption","en")] = "Subjects list"

trans_dict[("settings_caption","ru")] = "Настройки"
trans_dict[("settings_caption","de")] = "Einstellungen"
trans_dict[("settings_caption","en")] = "Settings"

trans_dict[("caption_correct","ru")] = "Правильных ответов"
trans_dict[("caption_correct","de")] = "Richtige Antworte"
trans_dict[("caption_correct","en")] = "Correct answers"

trans_dict[("caption_incorrect","ru")] = "Неправильных ответов"
trans_dict[("caption_incorrect","de")] = "Falshe Antworte"
trans_dict[("caption_incorrect","en")] = "Incorrect answers"



if __name__ == "__main__":
    fields = trans_dict.keys()
    fields_ru = [field for field in fields if field[1]=="ru"]
    for f in fields_ru:
        print(trans_dict[f])


