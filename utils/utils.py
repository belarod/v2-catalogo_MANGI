import os
import time

class Utils:
    
    @staticmethod
    def int_input(msg):
        '''Função que pede input, com loop até ser válida, mensagem e confirma se é um valor INTEIRO. (msg)'''
        valid_option = False
        result = None
        
        while not valid_option:
            try:
                value = input(msg)
                result = int(value)
                valid_option = True
            except:
                print('Deve ser um número inteiro, tente novamente.')
        return result
    
    @staticmethod
    def str_no_digit_input(msg):
        '''Função que pede input, com loop até ser válida, mensagem e confirma se é uma string SEM digitos. (msg)'''
        valid_option = False
        result = None
        
        while not valid_option:
            value = input(msg)
            
            if value and not any(char.isdigit() for char in value):
                result = value
                valid_option = True
            else:
                print('A entrada não pode conter números, tente novamente.')
        return result
    
    @staticmethod
    def clear_screen():
        '''Limpa terminal'''
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def sleep(seconds):
        '''Time'''
        if seconds < 0:
            raise ValueError("O tempo deve ser um valor não negativo.")
        if os.name == 'posix':
            os.system(f"sleep {seconds}")
        elif os.name == 'nt':
            os.system(f"timeout {seconds}")
        else:
            pass