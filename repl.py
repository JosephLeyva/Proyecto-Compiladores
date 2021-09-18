import lang

while True:
    texto = input('> ')
    resultado,error = lang.run(texto)

    if error: print(error.mostrar_error())
    else: print(resultado)