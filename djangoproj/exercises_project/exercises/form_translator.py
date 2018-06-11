__author__ = 'blazko'
translator = {}
base_translator = {}

#Teksti, ki se pojavljajo na vsaki strani, ker je base.html osnova za vse
base_translator[("base.html","ru","VAJE_IZ")] = "Упражнения"
base_translator[("base.html","de","VAJE_IZ")] = "Übungen"
base_translator[("base.html","en","VAJE_IZ")] = "Exercises"
base_translator[("base.html","ru","Domov")] = "Главная"
base_translator[("base.html","de","Domov")] = "Home"
base_translator[("base.html","en","Domov")] = "Home"
base_translator[("base.html","ru","Prijava")] = "Авторизация"
base_translator[("base.html","de","Prijava")] = "Log in"
base_translator[("base.html","en","Prijava")] = "Log in"
base_translator[("base.html","ru","Registracija")] = "Регистрация"
base_translator[("base.html","de","Registracija")] = "Register"
base_translator[("base.html","en","Registracija")] = "Register"
base_translator[("base.html","ru","Admin")] = "Администрация"
base_translator[("base.html","de","Admin")] = "Admin"
base_translator[("base.html","en","Admin")] = "Admin"


translator[("exercise_solve.html","ru","Check")] = "Проверить!"
translator[("exercise_solve.html","de","Check")] = "Prüfen!"
translator[("exercise_solve.html","en","Check")] = "Check!"

translator[("exercise_check.html","ru","Here_are_the_results_of")] = "Результаты упражнения"
translator[("exercise_check.html","de","Here_are_the_results_of")] = "Ergebnisse der Übung"
translator[("exercise_check.html","en","Here_are_the_results_of")] = "Results of exercise"
translator[("exercise_check.html","ru","Nazaj_na_vajo")] = "Повторить упражнение"
translator[("exercise_check.html","de","Nazaj_na_vajo")] = "Übung viderholen"
translator[("exercise_check.html","en","Nazaj_na_vajo")] = "Repeat exercise"


translator[("exercise_list.html","ru","Seznam_vaj")] = "Список упражнений"
translator[("exercise_list.html","de","Seznam_vaj")] = "Übungslist"
translator[("exercise_list.html","en","Seznam_vaj")] = "List of exercise"
translator[("exercise_list.html","ru","Nova_vaja")] = "Создать новое упражнение"
translator[("exercise_list.html","de","Nova_vaja")] = "Neue Übung "
translator[("exercise_list.html","en","Nova_vaja")] = "Make new exercise"
translator[("exercise_list.html","ru","Nova_tema")] = "Создать новую тему"
translator[("exercise_list.html","de","Nova_tema")] = "Neues Thema"
translator[("exercise_list.html","en","Nova_tema")] = "New subject"
translator[("exercise_list.html","ru","Edit")] = "Редактировать"
translator[("exercise_list.html","de","Edit")] = "Übung bearbaiten"
translator[("exercise_list.html","en","Edit")] = "Edit exercise"
translator[("exercise_list.html","ru","Solve")] = "Решить"
translator[("exercise_list.html","de","Solve")] = "Übung lösen"
translator[("exercise_list.html","en","Solve")] = "Solve exercise"


translator[("exercise_form.html","ru","nova_vaja")] = "Создать новое упражнене"
translator[("exercise_form.html","de","nova_vaja")] = "Neue Übung"
translator[("exercise_form.html","en","nova_vaja")] = "New exercise"
translator[("exercise_form.html","ru","save")] = "Сохранить"
translator[("exercise_form.html","de","save")] = "Speichern"
translator[("exercise_form.html","en","save")] = "Save"


translator[("subject_form.html","ru","nova_tema")] = "Создать новую тему"
translator[("subject_form.html","de","nova_tema")] = "Neuse Teme kreieren"
translator[("subject_form.html","en","nova_tema")] = "Create new subject"
translator[("subject_form.html","ru","Create")] = "Создать"
translator[("subject_form.html","de","Create")] = "Kreieren"
translator[("subject_form.html","en","Create")] = "Create"


def add_translated_strings(context_dict,
                           form_name,
                           language,
                           *translate_string):

    for s in translate_string:
        context_dict[s] = translator.get((form_name,language,s),s)

    for s in ("VAJE_IZ", "Domov", "Prijava", "Registracija", "Admin"):
        context_dict[s] = base_translator.get(("base.html",language,s),s)

