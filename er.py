#!/bin/python3
# -*- coding: utf-8 -*-
VERSION = '1.1v'
COPYRIGHT = 'GNU GENERAL PUBLIC LICENSE or GNU'


import sys
import codecs
import os
from os import system
import io
import signal
import importlib
import re
from colorama import Fore, Style, init

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


help_tutor = '''
Commands available in the text editor:

### Write Mode (p)
- p [ARGV]                    : Enter write mode
  - a [ARGV]                  : Append text to the current file
  - w [ARGV] (default)        : Save current text to [argv]. If the file exists, it will be overwritten; if not, a new file is created
    ### Command
    - .                                   : To write commands as text
    - *r*                                 : Reload the current text
    - *!* [COMMAND]                       : Execute a shell command
    - *s* [OLD TEXT] [NEW TEXT]           : Fade [OLD TEXT] to [NEW TEXT]
    - *u* [ARGV]                          : Delete the last line of text, [ARGV] must be a number, this is how many lines to delete
    - *q* [FILE] [ENCODING] [MODE]        : Save the text to [FILE] and exit
    - *w* [FILE] [ENCODING] [MODE]        : Save the current text to [FILE]
        - [FILE] if there is a '!' instead of the file, then it is not saved

        - [ENCODING] Encoding options:
          1: UTF-8
          2: UTF-16
          3: UTF-32
          4: Windows-1251
          5: ISO-8859-1
          6: ASCII
        - Default: UTF-8 if no encoding is specified

        -[MODE] Write mode:
            1: a       : append
            2: w       : write  (Default)

    ### Autosave
    - *a* [ARGV] [FILE]*         : Enable or disable autosaving. Default encoding is UTF-8, and default file for autosave is 'file_autosave.tmp'
        - [ARGV] on                : Enable autosave
        - [ARGV] off               : Disable autosave

    ### Plugin Management
        - *pgl* [FILE PYTHON]       : Load a Python file as a plugin, If your plugin to be loaded is in a different directory, for example plugin/plugin.py, then plugin.plugin
        - *pg* [FILE PYTHON]        : Run the main function of the loaded plugin, If your plugin is located in a different directory, for example plugin/plugin.py, then plugin.plugin
        - *pgd* [FILE PYTHON]       : Unload the specified plugin
        - *pgp*                     : Print all loaded plugins

    ### Command History
        - *pc*                       : Print the history of shell commands executed

    ### Syntax
        - *syntax* [ARGV] [FILE]
            - on  [FILE]             : ON syntax, glory who acts backlight
            - off                    : OFF syntax

    ### File load
        - *fl* [FILE]                : Flie load

### Read Mode (r)
- r [FILE] [ENCODING]     : Read [FILE] and display its contents on the screen
    - [ENCODING] Encoding options:
        - 1: UTF-8
        - 2: UTF-16
        - 3: UTF-32
        - 4: Windows-1251
        - 5: ISO-8859-1
        - 6: ASCII
        - 7: BINARY
    - Default: UTF-8 if no encoding is specified

### Miscellaneous
- h                       : Display this help information
- v                       : Show the version of the program
- q                       : Exit the editor
- ![COMMAND]              : Command shell
'''



class write_code:
    def __init__(self):
        self.index_coding = 0
        self.all_coding = ['utf-8', 'utf-16', 'utf-32', 'cp1251','iso-8859-1', 'ascii']
        self.s = 1
        self.text = ''
        self.text_undo = ''
        self.text_tmp = ''
        self.clear = 'cls' if os.name == 'nt' else 'clear'
        self.file_autosave = 'file_autosave.tmp'
        self.autosave = True
        self.history_command = []
        self.plg = []
        self.module_stek = []
        self.syntax_name = []
        self.syntax = False
        self.auto_load_syntax_file =  os.getenv("HOME") + '/' + '.syntax'

    def write_autosave(self, *argv):

        value = self.text_tmp.split()

        if not value:
            return

        write_file_on = False
        if len(value) >= 2:
            if value[0] == '*a*':
                if value[1]:
                    if value[1] == 'on':
                        self.autosave = True
                        write_file_on = True
                    elif value[1] == 'off':
                        self.autosave = False
                    else:
                        print('?')

        if self.autosave:
            try:
                self.file_autosave = value[2]
            except IndexError:
                pass

            if write_file_on:
                with open(self.file_autosave, 'w', encoding=self.all_coding[0]) as file:
                    file.write(str(self.text))
        else:
            if os.path.exists(self.file_autosave):
                os.remove(self.file_autosave)

    def write_search_and_replace(self):

        old_text = self.text_tmp.split()[1]
        new_text = self.text_tmp.split()[2]

        if old_text in self.text:
            self.text = self.text.replace(old_text, new_text)
            print(f'Replaced "{old_text}" with "{new_text}"')
        else:
            print(f'Text "{old_text}" not found')


    def write_plugin_print(self):
        system(self.clear)
        print('Loaded plugin:')
        for pl in self.plg:
            print(f'\t{pl}')
        continue_code()

    def write_plugin_load(self):
        val = self.text_tmp.split()[1]

        for tmp in self.plg:
            if val == tmp:
                print('?: This module is loaded')
                continue_code()
                self.write_reload()
                return

        if val[0] == '.':
            val = val[1:]

        try:
            self.module_stek.append(importlib.import_module(val))
            self.plg.append(val)
            print('OK')
        except ModuleNotFoundError:
            print('?: Plugin not Found')

        continue_code()
        system(self.clear)
        self.write_reload()

    def write_plugin(self):
        val = self.text_tmp.split()[1]
        s = 0

        system(self.clear)

        for pg in self.plg:
            if val == pg:
                try:
                    self.module_stek[s].main()
                except Exception as e:
                    print(f'Error: {e}')
            else:
                s += 1
        else:
            continue_code()


    def write_plugin_del(self):
        value = self.text_tmp.split()
        i = 0
        flag = False

        if value[1]:
            for pg in self.plg:
                if value[1] == pg:
                    del self.plg[i]
                    flag = True
                else:
                    i+=1
            else:
                if flag:
                    print('Del plugin')
                else:
                    print('?: Not plugin')
        else:
            print('?')


    def write_syntax(self, p=False):
        text1 = ''

        for s in self.text.splitlines():
            line_with_syntax = ''
            temp_word = ''

            for char in s:
                if char == '\t':
                    line_with_syntax += '\t'
                    continue

                if char.isspace():
                    if temp_word:
                        if temp_word in self.syntax_name:
                            line_with_syntax += (Fore.RED + temp_word + Style.RESET_ALL)
                        else:
                            line_with_syntax += temp_word
                        temp_word = ''
                    line_with_syntax += char
                else:
                    temp_word += char


            if temp_word:
                if temp_word in self.syntax_name:
                    line_with_syntax += (Fore.RED + temp_word + Style.RESET_ALL)
                else:
                    line_with_syntax += temp_word

            text1 += line_with_syntax + '\n'


        if p:
            text = io.StringIO(text1)
            self.s = 0
            for _, line in enumerate(text.readlines()):
                self.s += 1
                print(f'{self.s}: {line}', end='')
            self.s += 1



    def write_syntax_on(self):
        if len(self.text_tmp.split()) > 3:
            print('?')
            return

        if self.text_tmp.split()[1] == 'on':
            if len(self.text_tmp.split()) >= 3:
                if os.path.exists(self.text_tmp.split()[2]):
                    with open(self.text_tmp.split()[2], 'r') as f:
                        self.syntax_name = f.read().split()
                        self.syntax = True
        elif self.text_tmp.split()[1] == 'off':
            print('sd')
            self.syntax = False
        else:
            print('?')


    def write_auto_load_syntax(self):
        if os.path.exists(self.auto_load_syntax_file):
            with open(self.auto_load_syntax_file, 'r', encoding='UTF-8') as f:
                self.syntax_name = f.read().split()
                self.syntax = True



    def write_reload(self):
        system(self.clear)
        text = io.StringIO(self.text)

        if self.syntax:
            self.write_syntax(p=True)
            return

        self.s = 0
        for _, line in enumerate(text.readlines()):
            self.s += 1
            print(f'{self.s}: {line}', end='')
        self.s += 1

    def write_print_command(self):
        os.system(self.clear)
        for i in self.history_command:
            print(*i)

        continue_code()
        self.write_reload()


    def write_command(self):
        command = self.text_tmp.split()[1:]

        self.history_command.append(' '.join(command))
        system(self.clear)
        try:
            system(' '.join(command))
        except KeyboardInterrupt:
            self.write_reload()
            return

        continue_code()

        self.write_reload()

    def write_encoding(self):
        try:

            if len(self.text_tmp.split()) < 2:
                self.all_coding = 0

            if not self.text_tmp.split()[2].isdigit():
                return 1

            if len(self.all_coding) >= int(self.text_tmp.split()[2])-1 or int(self.text_tmp.split()[2]) >= -1:
                self.index_coding = int(self.text_tmp.split()[2]) - 1
            else:
                self.index_coding = 0
        except:
            self.index_coding = 0

    def write_reload_text_file(self):
        if len(self.text_tmp.split()) == 2:
            if os.path.exists(self.text_tmp.split()[1]):
                with open(self.text_tmp.split()[1], 'r', encoding=self.all_coding[self.index_coding], errors='replace') as f:
                    self.text = f.read()
            else:
                print('?: Not File')
        else:
            print('?: Not argument')
        continue_code()

    def write_update(self, mode='w'):
        if len(self.text_tmp.split()) < 2:
            self.all_coding = 0

        with codecs.open(self.text_tmp.split()[1], mode, encoding=self.all_coding[self.index_coding], errors='replace') as f:
            f.seek(0)
            f.write(self.text)
            f.seek(0)
        with codecs.open(self.text_tmp.split()[1], 'r', encoding=self.all_coding[self.index_coding], errors='replace') as f:
            self.text = f.read()
        system(self.clear)
        self.write_reload()



    def write_quit(self, mode='w'):
        returncode = '1'
        signal.alarm(0)

        try:

            if self.text_tmp.split()[1] == '!' or not self.text_tmp.split()[1].strip():
                return ('file: close | code: ' + str(returncode))

            with codecs.open(self.text_tmp.split()[1], mode, encoding=self.all_coding[self.index_coding], errors='replace') as file:
                file.write(str(self.text))
                returncode = '0'
                print('Done!')
                self.text = ''
                return ('file: ' + (self.text_tmp.split()[1]) + ' | code: ' + returncode)

        except IndexError:

            if self.text_tmp:
                return ('file: close | code: ' + str(returncode))

        except PermissionError:
            print('?:Access denied')
        except OSError:
            print('?:Access denied is os')

    def write_undo(self):

        if len(self.text_tmp.split()) == 2:
            if self.text_tmp.split()[1].isdigit():
                s_undo = int(self.text_tmp.split()[1])
            else:
                return
        else:
            s_undo = 1

        s_undo_m = '-' + str(s_undo)
        s_undo_m = int(s_undo_m)

        if self.s > 1:
            self.s -= s_undo
            text = io.StringIO(self.text)
            text_tmp = text.readlines()
            text_tmp = text_tmp[:s_undo_m]
            self.text = ''.join(text_tmp)
            self.write_reload()

    def write_mode(self, mode = 'w'):
        system(self.clear)
        self.text = ''
        returncode = '1'

        self.write_auto_load_syntax()
        while True:
            try:

                signal.signal(signal.SIGALRM, self.write_autosave)
                signal.alarm(15)
                self.text_tmp = str(input(f'{self.s}: '))
            except KeyboardInterrupt:
                self.write_autosave()
                return ('\nfile: close | code: ' + str(returncode))

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
                elif self.text_tmp.split()[0] == '*s*':
                    self.write_search_and_replace()
                elif self.text_tmp.split()[0] == '*pc*':
                    self.write_print_command()
                elif self.text_tmp.split()[0] == '*pgl*':
                    self.write_plugin_load()
                elif self.text_tmp.split()[0] == '*pg*':
                    self.write_plugin()
                elif self.text_tmp.split()[0] == '*pgp*':
                    self.write_plugin_print()
                elif self.text_tmp.split()[0] == '*pgd*':
                    self.write_plugin_del()
                elif self.text_tmp.split()[0] == '*syntax*':
                    self.write_syntax_on()
                elif self.text_tmp.split()[0] == '*fl*':
                    self.write_reload_text_file()
                elif self.text_tmp[0] == '.':
                    self.text_tmp = self.text_tmp[1:]
                    self.text += (self.text_tmp + '\n')
                    self.s += 1
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
            except:
                print('Error')
                exit()

            self.index_coding = 0
            self.write_reload()


    def __del__(self):
        print('Bye')

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

    def __del__(self):
        print('Bye')

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
            print('?: Not argument')
            return

    elif value[0] == '!':

        if len(value.split()) >= 0:
            system(value[1:])
        else:
            print(value.split())
            print('?: Not argument')

    elif value.split()[0] == 'q':
        exit()
    elif value.split()[0] == 'v':
        print(VERSION)
    elif value.split()[0] == 'h':
        print(help_tutor)
    elif value.split()[0] == 'c':
        system('cls' if os.name == 'nt' else 'clear')
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


def continue_code():
    try:
        print('\n\nPress <ENTER> to continue\n\n')
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    try:
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


