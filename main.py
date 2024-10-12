import tkinter
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog as fd


class Window(tkinter.Tk):
    """Класс текстового редактора, наследуется от базового класс Tk модуля tkinter"""
    def __init__(self, width=200, height=100):
        """Конструктор класса"""
        super().__init__()
        self.__width = width        # ширина окна
        self.__height = height      # высота окна
        self.__data = ""            # атрибут для хранения данных

        self.__set_window_center_screen(self.__width, self.__height)    # метод устанавливает окно по центру экрана
        self.__set_main_menu()      # метод создает меню

        self.title('Текстовый редактор')    # заголовок окна
        # создание виджета Text вместе со scroll barjv из модуля ScrolledText
        self.text_edit = ScrolledText(self, bd=2, bg='#fbfdcc', fg='blue', font="Arial 12", wrap="word", padx=10)


    def __set_main_menu(self):
        """Метод создания меню"""
        main_menu = tkinter.Menu()      # создаем объект меню
        self.config(menu=main_menu)     #
        file_menu = tkinter.Menu(tearoff=0)

        # создаем подменю пункта меню Файл
        file_menu.add_command(label='Открыть файл', command=self.__open_file)
        file_menu.add_command(label='Сохранить файл как', command=self.__save_file)
        file_menu.add_separator()
        file_menu.add_command(label='Закрыть редактор', command=self.destroy)

        # создаем подменю пункта меню Редактировать
        edit_menu = tkinter.Menu(tearoff=0)
        edit_menu.add_cascade(label='Вырезать текст', command=self.__cut_text)
        edit_menu.add_cascade(label='Копировать текст', command=self.__copy_text)
        edit_menu.add_cascade(label='Вставить текст', command=self.__paste_text)
        edit_menu.add_cascade(label='Удалить текст', command=self.__clear_text)

        # Устанавливаем пункты меню вместе с пунктами подменю
        main_menu.add_cascade(label='Файл', menu=file_menu)
        main_menu.add_cascade(label='Редактирование', menu=edit_menu)

    def __set_window_center_screen(self, width, height):
        """Метод рассчитывает положение приложения на экране
        и устанавливает положение приложения по центру экрана,
        где width - ширина, а height - высота приложения"""
        sw = self.winfo_screenwidth()  # получим ширину экрана монитора
        sh = self.winfo_screenheight()  # получим высоту экрана монитора
        x = (sw - width) / 2
        y = (sh - height) / 2
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def __open_file(self):
        """Метод открывает диалоговое окно выбора файла и возвращает имя выбранного файла (строку)
        или пустую строку. Если файл выбран, его данные считываются в виджет Text """
        filetypes = (
            ('Текстовый файл', '*.txt'),)
        # ('All files', '*.*'))
        file_name = fd.askopenfilename(initialdir=".\\", title="Выберите файл", filetypes=filetypes)
        if file_name != '':
            text = ''
            #file_name = file_name.replace('/', '\\')
            try:
                with open(file_name, 'r', encoding='utf8') as file:
                    text = file.read()
            except:
                s = 'Ошибка при открытии и чтении файла'

            self.text_edit.delete('1.0', tkinter.END)
            self.text_edit.insert('1.0', text)

    def __save_file(self):
        """Метод открывает диалоговое окно сохранения файла и возвращает имя файла (строку)
        или пустую строку. Если имя файла не пустая строка, данные считываются из виджета Text и сохраняются в файл """
        filetypes = (
            ('Текстовый файл', '*.txt'),)
        # ('All files', '*.*'))
        file_name = fd.asksaveasfilename(initialdir=".\\", title='Сохраните файл', filetypes=filetypes)
        if file_name != "":
            text = self.text_edit.get('1.0', tkinter.END)
            try:
                with open(file_name, 'w', encoding='utf8') as file:
                    file.write(text)

            except:
                s = 'Ошибка при открытии и сохранении файла'

    def __cut_text(self):
        """Метод вырезает блок выделенных данных и сохраняет их в приватном атрибуте __data.
        Выделенный блок данных удаляется из виджета Text"""
        if self.text_edit.selection_get():
            self.__data = self.text_edit.selection_get()
            self.text_edit.delete('sel.first', 'sel.last')

    def __copy_text(self):
        """Метод получает блок выделенных данных и сохраняет их в приватном атрибуте __data"""
        if self.text_edit.selection_get():
            self.__data = self.text_edit.selection_get()

    def __paste_text(self):
        """Метод получает блок данных из приватного атрибута объекта __data и вставляет их в виджет Text в позицию,
        где находится курсов"""
        cur_position = self.text_edit.index(tkinter.INSERT)
        self.text_edit.insert(cur_position, self.__data)

    def __clear_text(self):
        """Метод удаляет все данные из виджета Text"""
        self.text_edit.delete('1.0', tkinter.END)

if __name__ == '__main__':
    window = Window(800, 600)       # создаем объект главного окна с указанными размерами
    window.text_edit.pack(fill='both', expand=1)    # помещаем главное окно в менеджер пакетов

    window.mainloop()
