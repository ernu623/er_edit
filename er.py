#!/bin/python3
# -*- coding: utf-8 -*-
VERSION = '1.1v'
COPYRIGHT = 'GNU GENERAL PUBLIC LICENSE or GNU'


import sys # импорт для достпуа внешная аргмента как python er.py -p a
import codecs # импорт для нормалная кодеровка текста в файле
import os
from os import system # импорт для system и os.name для очиски экрана
import io
import signal


#тутор нахуй 
help_tutor = '''
p   [argv]  Mode wrtie
    a [argv]                    Will complement the text
    w [argv] default            If not, creates a new file, if there is a file, it is recreated
    *r*                         Reload text
    *!* [COMMAND]               Command is shell
    *u*                         Delete lines of text
    *q* [FILE] [ENCODING]       Save in file [FILE] and exit
    *w* [FILE] [ENCODING]       If not file, creates a now, or not quit

        1-6 [ENCODING]      Encodind write for file
              1         2        3          4                 5            6
            UTF-8    UTF-16   UTF-32    Windows-1251     ISO-8859-1      ASCII
           default
    *a* [ARGV] [FILE]           Autosave, default encoding UTF-8, default file autosave 'file_autosave.tmp'
        on                         on autosave
        off                        off autosave

r   [FILE] [ENCODING]           Mode read
    It reads [FILE] and shows the screen

        1-7, b [ENCODING]      Encodind read for file
              1         2        3          4                 5            6          b
            UTF-8    UTF-16   UTF-32    Windows-1251     ISO-8859-1      ASCII      BINARY
           default

h   Help program

v   Version program

q   The exit
'''


# еще один тутор нахуй, но для внешная аргумента, кстати у меня хорошо с англики, но все это переводчик сделол
help_argv = '''
This is a simple file editor

er [ARGV] [FILE]

    -v version
    -c copyright
    -h help
         1      2
    -p [ARGV] [FILE] mode wrtie
        a [ARGV]            Will complement the text, if not file, it is creates
        w [ARGV] default    If not, creates a new file, if there is a file, it is recreated
            [ENCODING]
            default 1
              1         2        3          4                 5            6
            UTF-8    UTF-16   UTF-32    Windows-1251     ISO-8859-1      ASCII
    -r [FILE] [ARGV] [ENCODING] mode read
        b [ARGV]            read file mode binar
'''

class write_code: # класс для запиас
    def __init__(self):
        # обычая инид
        self.index_coding = 0 # перемена для какой имына кодеровка выберет
        self.all_coding = ['utf-8', 'utf-16', 'utf-32', 'cp1251','iso-8859-1', 'ascii'] # список кодеровка
        self.s = 1 # строка
        self.text = '' # сам текст
        self.text_undo = '' # текст но одну строк менше 
        self.text_tmp = '' # хуй его знает для это нахуй
        self.clear = 'cls' if os.name == 'nt' else 'clear'
        self.file_autosave = 'file_autosave.tmp'
        self.autosave = True

    # мне подло еще миллард строк комент писать

    def write_autosave(self, *argv):
        value = self.text_tmp.split()

        try:
            if value[1]:

                if value[1] == 'on':
                    self.autosave = True
                elif value[1] == 'off':
                    self.autosave = False
                else:
                    print('?')

        except IndexError:
            pass

        if self.autosave:
            try:
                self.file_autosave = value[2]
            except IndexError:
                pass

            with open(self.file_autosave, 'w', encoding=self.all_coding[0]) as file:
                file.write(str(self.text))
        else:
            if os.path.exists(self.file_autosave):
                os.remove(self.file_autosave)

    def write_reload(self):
        system(self.clear)
        text = io.StringIO(self.text)

        o= 1
        for _, line in enumerate(text.readlines()):
            print(f'{o}: {line}', end='')
            o += 1


    def write_command(self):
        import subprocess
        command = self.text_tmp.split()[1:]

        try:
            result = subprocess.run(command, capture_output=True, shell=True)
        except KeyboardInterrupt:
            self.write_reload()
            return

        subprocess.run([self.clear])

        print(result.stdout.decode())
        print(result.stderr.decode())
        print(result.returncode)

        input('Press <ENTER> to continue')
        subprocess.run([self.clear])

        self.write_reload()
        del subprocess

    def write_encoding(self):
        try:

            if len(self.all_coding) >= int(self.text_tmp.split()[2]) or int(self.text_tmp.split()[2]) >= -1:
                self.index_coding = int(self.text_tmp.split()[2])
                print('s')
            else:
                return 1

        except ValueError:
            return 1
        except IndexError:
            return
        except:
            return 1

    def write_update(self):
        with codecs.open(self.text_tmp.split()[1], 'w', encoding=self.all_coding[self.index_coding], errors='replace') as f:
            f.seek(0)
            f.write(self.text)

        system(self.clear)
        self.write_reload()


    def write_quit(self, mode): # ну конечно я говнокодер, не буду это перепишит
        returncode = '1'
        signal.alarm(0)

        try:

            if self.text_tmp.split()[1] == '!':
                return ('file: close | code: ' + str(returncode))

            with codecs.open(self.text_tmp.split()[1], mode, encoding=self.all_coding[self.index_coding], errors='replace') as file:
                file.write(str(self.text).encode(self.all_coding[self.index_coding]))
                returncode = '0'
                print('Done!')
                self.text = ''
                return ('file: ' + (self.text_tmp.split()[1]) + ' | code: ' + returncode)
        except IndexError:

            if not self.text_tmp:
                self.text += '\n'
                self.s += 1
                return
            else:
                print('?')
                return

        except PermissionError:
            print('Access denied')
        except OSError:
            print('Access denied is os')

    def write_undo(self): # это тоже не буду перепишит
        system(self.clear)
        if self.s > 1:
            self.s -= 1

            all_lines = self.text.strip().split('\n')
            self.text_undo = '\n'.join(all_lines[:self.s])
            self.text = str(self.text_undo)

            for idx, line in enumerate(all_lines[:self.s], 1):
                if line:
                    print(f'{idx}: {line}')
                else:
                    print(f'{idx}: ')



    def write_mode(self, mode = 'w'):
        system(self.clear)
        self.text = ''
        returncode = '1'

        while True:
            try:

                signal.signal(signal.SIGALRM, self.write_autosave)
                signal.alarm(15)
                self.text_tmp = str(input(f'{self.s}: '))
                signal.alarm(0)

            except KeyboardInterrupt:
                self.write_autosave()
                print('\n')
                return
            try:
                if self.text_tmp.split()[0] == '*q*':
                    res = self.write_encoding()

                    if res == 1:
                        return '?'

                    result = self.write_quit(mode)
                    return result
                elif self.text_tmp.split()[0] == '*w*':
                    res = self.write_encoding()

                    if res == 1:
                        return '?'

                    self.write_update()
                elif self.text_tmp.split()[0] == '*u*':
                    self.write_undo()
                elif self.text_tmp.split()[0] == '*!*':
                    self.write_command()
                elif self.text_tmp.split()[0] == '*r*':
                    self.write_reload()
                elif self.text_tmp.split()[0] == '*a*':
                    self.write_autosave()
                else:
                    self.text += (self.text_tmp + '\n')
                    self.s += 1
            except IndexError:

                if not self.text_tmp.split():
                    self.text += '\n'
                    self.s += 1
                else:
                    print('?')

            except IsADirectoryError:
                print('Unavailable titles')
            #except:
                #print('Error')
                #exit()
            finally:
                self.index_coding = 0


class read_mode:
    def __init__(self, file_name: str, b=False, index=1, code=0):
        self.text = ''
        self.name_file = file_name

        if int(code) > 0:
            self.index_coding = int(code) - 1
        else:
            self.index_coding = 0

        self.all_coding = ['utf-8', 'utf-16', 'utf-32', 'cp1251', 'iso-8859-1', 'ascii']
        self.flag_bin = b

        try:
            if self.flag_bin:
                file = open(self.name_file, 'rb')
            else:
                file = open(self.name_file, 'r', encoding=self.all_coding[self.index_coding])
        except FileNotFoundError:
            print('?')
            return
        except:
            print('?')

        try:
            self.text = file.read()
        except UnicodeDecodeError:
            file.close()
            self.flag_bin = True
            file = open(self.name_file, 'rb')
            self.text = file.read()
        finally:
            file.close()

        self.name_os = 'cls' if os.name == 'nt' else 'clear'

    def read_file(self):
        len_coding = len(self.all_coding)

        if self.index_coding > len_coding:
            print('?')
            return

        if self.index_coding <= -1:
            print('?')

            print(self.index_coding)
            return

        try:
            print('---***---')
            print(self.text if not self.flag_bin else repr(self.text))
            print('---***---')
            print(f'File name: {self.name_file}')
            print(f'Length: {len(self.text)}')
            print(f'Encoding: {self.all_coding[self.index_coding] if not self.flag_bin else "binary"}')
            if self.flag_bin:
                print('Warning: opened in binary mode due to encoding issues.')
            print('Done!')
        except keyboardinterrupt:
            print('exit\n')


def mode(value: str):
    global version
    if value.split()[0] == 'p':
        try:
            result = write_code().write_mode(mode=value.split()[1])
        except IndexError:
            result = write_code().write_mode()

        print(result)

    elif value.split()[0] == 'r':
        try:
            try:

                if value.split()[2] == 'b':
                    read_mode(value.split()[1], b=true).read_file()

                else:
                    try:
                        read_mode(value.split()[1], code=value.split()[2]).read_file()
                    except IndexError:
                        read_mode()(value.split()[1]).read_file()

            except IndexError:
                read_mode(value.split()[1]).read_file()

        except IndexError:
            print('?')
            return

    elif value.split()[0] == 'q':
        exit()
    elif value.split()[0] == 'v':
        print(VERSION)
    elif value.split()[0] == 'h':
        print(help_tutor)
    elif value.split()[0] == 'c':
        system('cls' if name == 'nt' else 'clear')
    else:
        print('?')


def main():
    print('h - help')
    while True:
        while True:
            try:
                text = input('> ')
            except KeyboardInterrupt:
                print('\n')
                return
            if not text:
                print('?')
            else:
                break
        mode(text)


if __name__ == '__main__':
    try: # мне падло переписать это
        if 4 < len(sys.argv):
            print(help_argv)
            exit()

        if sys.argv[1] == '-v':
            print(VERSION)
        elif sys.argv[1] == '-c':
            print(COPYRIGHT)
        elif sys.argv[1] == '-h':
            print(help_argv)
        elif sys.argv[1] == '-p':
            w = write_code()

            try:
                result = w.write_mode(sys.argv[2])
            except IndexError:
                result = w.write_mode('w')

            print(result)

        elif sys.argv[1] == '-r':
            try:
                try:

                    if sys.argv[3] == 'b':
                        read_mode(sys.argv[2], b=True).read_file()
                    elif type(int(sys.argv[3])) == int:
                        read_mode(sys.argv[2], code=sys.argv[3]).read_file()
                    else:
                        print(help_argv)

                except IndexError:
                    read_mode(sys.argv[2]).read_file()
                except ValueError:
                    print(help_argv)
            except IndexError:
                print(help_argv)

        else:
            print(help_argv)

    except IndexError:
        main()


