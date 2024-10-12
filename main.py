import tkinter
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog as fd


class Window(tkinter.Tk):
    def __init__(self, width=200, height=100):
        super().__init__()
        self.__width = width
        self.__height = height
        self.__data = ""

        self.__set_window_center_screen(self.__width, self.__height)
        self.__set_main_menu()

        self.title('Текстовый редактор')
        self.text_edit = ScrolledText(self, bd=2, bg='#fbfdcc', fg='blue', font="Arial 12", wrap="word", padx=10)


    def __set_main_menu(self):
        main_menu = tkinter.Menu()
        self.config(menu=main_menu)
        file_menu = tkinter.Menu(tearoff=0)
        file_menu.add_command(label='Открыть файл', command=self.__open_file)
        file_menu.add_command(label='Сохранить файл как', command=self.__save_file)
        file_menu.add_separator()
        file_menu.add_command(label='Закрыть редактор', command=self.destroy)

        edit_menu = tkinter.Menu(tearoff=0)
        edit_menu.add_cascade(label='Вырезать текст', command=self.__cut_text)
        edit_menu.add_cascade(label='Копировать текст', command=self.__copy_text)
        edit_menu.add_cascade(label='Вставить текст', command=self.__paste_text)
        edit_menu.add_cascade(label='Удалить текст', command=self.__clear_text)

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
        if self.text_edit.selection_get():
            self.__data = self.text_edit.selection_get()
            self.text_edit.delete('sel.first', 'sel.last')

    def __copy_text(self):
        if self.text_edit.selection_get():
            self.__data = self.text_edit.selection_get()

    def __paste_text(self):
        cur_position = self.text_edit.index(tkinter.INSERT)
        self.text_edit.insert(cur_position, self.__data)

    def __clear_text(self):
        self.text_edit.delete('1.0', tkinter.END)

if __name__ == '__main__':
    window = Window(800, 600)

    window.text_edit.pack(fill='both', expand=1)

    window.mainloop()
