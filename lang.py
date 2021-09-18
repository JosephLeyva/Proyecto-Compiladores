from utileria import es_espacio

###############################
#        CONSTANTES
################################

DIGITOS = '0123456789'


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



###############################
#        TOKENS
################################

T_ENTERO     =   'entero'
T_REAL      =   'real'
T_MAS        =   'mas'
T_MENOS      =   'menos'
T_MULT       =   'multiplica'
T_DIV        =   'divide'
T_IZQ_PARENT =   'izq_parent'
T_DER_PARENT =   'der_parent'


class Token:
    def __init__(self,tipo,valor = None):
        self.tipo = tipo
        self.valor = valor
    def __repr__(self):
        if self.valor: return f'{self.tipo}: {self.valor}'
        return f'{self.tipo}'

###############################
#        LEXER
################################

class Lexer:
    def __init__(self,texto):
        self.texto = texto
        self.pos = -1   #Ver la posición actual (inicia en -1 para al avanzar agarrar el texto[0])
        self.caracter_actual = None  #Ver el caracter actual
        self.avanzar()

    def avanzar(self):
        '''Este método va a avanzar al siguiente caracter '''
        self.pos += 1
        # El caracter actual toma el caracter de la posicion siempre que sea menor a la longitud del texto dado
        self.caracter_actual = self.texto[self.pos] if self.pos < len(self.texto) else None

    def crear_tokens(self):
        '''Regresa una lista con los tokens encontrados'''
        tokens = []

        # mientras todavía existen caracteres por leer
        while self.caracter_actual != None:
            if es_espacio(self.caracter_actual):
                self.avanzar()
            elif self.caracter_actual in DIGITOS:
                tokens.append(self.crear_numero())
            elif self.caracter_actual == '+':
                tokens.append(Token(T_MAS))
                self.avanzar()
            elif self.caracter_actual == '-':
                tokens.append(Token(T_MENOS))
                self.avanzar()
            elif self.caracter_actual == '*':
                tokens.append(Token(T_MULT))
                self.avanzar()
            elif self.caracter_actual == '/':
                tokens.append(Token(T_DIV))
                self.avanzar()
            elif self.caracter_actual == '(':
                tokens.append(Token(T_IZQ_PARENT))
                self.avanzar()
            elif self.caracter_actual == ')':
                tokens.append(Token(T_DER_PARENT))
                self.avanzar()
            else:
                # Si no coincide el caracter regresamos un error
                caracter = self.caracter_actual
                self.avanzar()
                return [],ErrorCaraterIlegal("'" + caracter  + "'")
            
        return tokens, None

    def crear_numero(self):
        '''Metodo que crea un numero flotante o entero'''
        num_str = ''
        conteo_puntos = 0
        
        while self.caracter_actual != None and self.caracter_actual in DIGITOS + '.':
            if self.caracter_actual == '.':
                if conteo_puntos == 1: break
                conteo_puntos += 1
                num_str += '.'
            else:
                num_str += self.caracter_actual

            self.avanzar()
        
        if conteo_puntos == 0:
            return Token(T_ENTERO, int(num_str))
        else:
            return Token(T_REAL,float(num_str))

###############################
#        RUN
################################

def run(texto):
    lexer = Lexer(texto)
    tokens,error  = lexer.crear_tokens()

    return tokens,error