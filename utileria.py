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
