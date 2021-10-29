import pandas as pd
import re
import utileria

df = pd.read_csv('TABLA_TRANSICIONES.csv')
df.drop(columns=['ESTADO'],inplace=True)

tabla_transicion= df.values.tolist()


Alfabeto = {c: i for i, c in enumerate(df.columns)}



TokenType = [
   None,
  'T_ENTERO',
  'T_MAS',
  'T_MENOS',
  'invalido',
  'T_MULT',
  'T_DIV',
  'T_MODULO',
  'T_EXP',
  'T_MENOR',
  'T_MAYOR',
  'T_IGUAL',
  'T_IZQ_PAREN',
  'T_DER_PAREN',
  'T_IZQ_CORCH',
  'T_DER_CORCH',
  'T_IZQ_LLAVE',
  'T_DER_LLAVE',
  'T_COMA',
  'T_NOT',
  'T_PUNTO_COMA',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_O',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_Y',
  'T_IDENTIFICADOR',
   None,
  'T_CADENA',
   None,
   None,
  'T_MENOR_IGUAL',
  'T_MAYOR_IGUAL',
  'T_IGUAL_IGUAL',
  'T_NOT_IGUAL',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_SI',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_FLOTANTE',
   None,
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_VAR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_NULO',
  'T_PARA',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_SINO',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_FALSO',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_ROMPER',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IDENTIFICADOR',
  'T_IMPRIMIR',
  'T_REGRESAR',
  'T_IDENTIFICADOR',
  'T_CONTINUAR',
  'T_VERDADERO',
  'T_IDENTIFICADOR']

class Token:
    def __init__(self,tipo,valor = None):
        self.tipo = tipo
        self.valor = valor
    def __repr__(self):
        if self.valor: return f'{self.tipo}: {self.valor}'
        return f'{self.tipo}'


estados_aceptacion = [True if tipo != None else False for tipo in TokenType]

###############################
#        ERROR
################################

class Error:
    def __init__(self,error,detalles):
        self.error = error
        self.detalles = detalles

    def mostrar_error(self):
        resultado = f'{self.error}: {self.detalles}'
        return resultado

class ErrorCaraterIlegal(Error):
    def __init__(self, detalles):
        super().__init__('Caracter Ilegal', detalles)



def es_espacio(c):
    if c in ' \t\r\n':
        return True
    return False

def es_nueva_linea(c):
    if c in '\n':
        return True
    return False

def es_delimitador(c):
    if (c == '+' or c == '-' or c == '*' or c == '/' or c == ',' or 
         c == ';' or c == '=' or c == '!' or c == '<' or c == '>' or c == '(' or c == ')' or
         c == '{' or c == '}' or c == '[' or c == ']' or c == '\0'):
         return True


    return False



class Lexer:
    def __init__(self,input):
        self.raw_input = input
        self.input_limpio = ""
        self.tokens = []

        self.inicio = 0
        self.actual = 0
        self.linea = 1

    def avanzar(self,espacios=1):
        '''
        Avanza el puntero del input n-espacios
        '''
        self.actual += espacios

    def regresar(self,espacios=1):
        '''
        Regresa el puntero del input n-espacios
        '''    
        self.actual -= espacios
    
    def recoger_caracter(self):
        '''
        Regresa el caracter donde nos encontremos
        '''
        return '\0' if self.es_final() else self.input_limpio[self.actual]

    def recoger_caracter_siguiente(self):
        '''
        Regresa el caracter que le sigue al que nos encontremos
        '''
        if self.actual + 1 >= len(self.input_limpio):
            return '\0'
        return self.input_limpio[self.actual+1]
    
    def recoger_caracter_anterior(self):
        '''
        Regresa el caracter anterior al que nos encontremos
        '''
        return self.input_limpio[self.actual-1]

    def avanzar_linea(self):
        '''
        Avanzamos una linea en el input
        '''
        self.linea+=1
    
    def es_final(self):
        '''
        Regresamos si ya alcanzamos el final del input o no
        '''
        return self.actual >= len(self.input_limpio)

    def quitar_espacios(self):
        '''

        for i in range(0,len(self.raw_input)):                      # Mantenemos un espacio
            if (self.raw_input[i] != ' ' and self.raw_input[i] != '\n' and self.raw_input[i] != '\t') or (i > 0 and self.raw_input[i-1] != ' ' and self.raw_input[i-1] != '\n' and self.raw_input[i-1] != '\t'):
                self.input_limpio += self.raw_input[i]
                
        return self.input_limpio
    '''

        pattern = r"(\".*?\")|(\s+$)"
        # first group captures quoted strings (double or single)
        # second group captures comments (//single-line or /* multi-line */)
        regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
        def _replacer(match):
            # if the 2nd group (capturing comments) is not None,
            # it means we have captured a non-quoted (real) comment string.
            if match.group(2) is not None:
                return "" # so we will return empty to remove the comment
            else: # otherwise, we will return the 1st group
                return match.group(1) # captured quoted-string
        self.input_limpio = regex.sub(_replacer, self.raw_input)
        
    def quitar_comentarios(self):
        pattern = r"(\".*?\")|(\|\-.*?\-\||#[^\r\n]*$)"
        # first group captures quoted strings (double or single)
        # second group captures comments (//single-line or /* multi-line */)
        regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
        def _replacer(match):
            # if the 2nd group (capturing comments) is not None,
            # it means we have captured a non-quoted (real) comment string.
            if match.group(2) is not None:
                return "" # so we will return empty to remove the comment
            else: # otherwise, we will return the 1st group
                return match.group(1) # captured quoted-string
        self.input_limpio =  regex.sub(_replacer, self.input_limpio)
        
 
    
    def scan_token(self):
        '''
        Agrega tokens encontrados
        '''
        # Al inicio nos encontramos en la posición 0
        # Vemos el caracter actual
        ch = self.recoger_caracter()
        state = 0
        token_aux = ''
        
        while (not self.es_final()):
            
            while es_espacio(ch):
                self.avanzar()
                ch = self.recoger_caracter()
            
            
                
               

            if self.es_final():
                break
            
                
            state = tabla_transicion[state][Alfabeto[ch]]
        
            if state == -1:
                if  es_delimitador(ch) or es_delimitador(self.recoger_caracter_anterior()) :
                    self.tokens.append(token_aux)
                    state = 0
                    self.regresar()
                
                
                else:
                    return [],ErrorCaraterIlegal("'" + ch  + "'")
                
                
               
            
            if estados_aceptacion[state]:
                token_aux = Token(TokenType[state])
                
            
            #print(f'ch: {ch}\tpos: {self.actual}\testado: {state}\ttoken_aux = {token_aux}')
            

            self.avanzar()
            ch = self.recoger_caracter()
            if es_espacio(ch):
                if estados_aceptacion[state]:
                    self.tokens.append(token_aux)
                    state = 0
                    
                    self.avanzar()
                    ch = self.recoger_caracter()
                    

        if estados_aceptacion[state]:
            self.tokens.append(token_aux)
        else:
            return [],ErrorCaraterIlegal("'" + ch  + "'")

        return self.tokens,None    
            


###############################
#        RUN
################################

def run(texto):
    lexer = Lexer(texto)
    lexer.quitar_comentarios()
    lexer.quitar_espacios()
    tokens,error  = lexer.scan_token()

    return tokens,error