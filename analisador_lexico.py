import json 

delimiter = {
    ':': 'dois-pontos',
    '{': 'abre-chaves',
    '}': 'fecha-chaves',
    '(': 'abre-parenteses',
    ')': 'fecha-parenteses',
    ',': 'virgula'
}
operators = {
    '+': 'operador-mais',
    '=': 'operador-igual',
    '!=': 'operador-diferente',
    '<': 'operador-menor'
}
groups = {
    0: 'nada',
    1: 'comentario',
    2: 'quebra-linha',
    3: 'identificador',
    4: 'logico',
    5: 'atribuicao',
    6: 'texto',
    7: 'numero',
    8: 'operador-diferente',
    9: 'desconhecido'
}
reservado = [ 'Funcao', 'Logica', 'Logico', 'Texto', 'Numero', 'se', 'se nao se', 'se nao', 'enquanto', 'retorna' ]

def analisadorLexico(programa):
    # TODO: implementar essa funcao

    global delimiter
    global operators
    global groups

    tokens = []
    erros = []
    lexeme = ''
    line = 1
    index = 0
    cur_index = 0
    search = 0

    saving_comment = False

    scape = 0

    for c in programa:
        inserted_delimiter = False
        #Comentario
        if c == '-':
            if search == 1:
                saving_comment = True
            elif search == 0:
                index = cur_index
                search = 1
                lexeme += c

        if search == 5 and c != ':':
            inserirToken(tokens, delimiter[":"], index, line, ':')
            search = 0
            lexeme = ''

        #Numero
        if search == 0 and c.isnumeric():
            search = 7
            lexeme += c
            index = cur_index
        elif search == 7 and not c.isnumeric():
            inserirToken(tokens, groups[7], index, line, lexeme)
            search = 0
            lexeme = ''
        elif search == 7:
            lexeme += c

        #Texto
        if search == 0 and c == "'":
            index = cur_index
            search = 6
            lexeme += c
        elif search == 6 and c == '#' and not scape:
            scape = True
            lexeme += c
        elif search == 6 and scape:
            scape = False
            lexeme += c
        elif search == 6 and c == "'":
            lexeme += c
            inserirToken(tokens, groups[6], index, line, lexeme)
            search = 0
            lexeme = ''
        elif search == 6 and not scape:
            lexeme += c
     
        #Logico
        if search == 0 and c.isupper():
            search = 4
            index = cur_index
            lexeme += c
        elif search == 4 and not c.isupper() and not c.islower():
            inserirToken(tokens, groups[4], index, line, lexeme)
            search = 0
            lexeme = ''
        elif search == 4:
            lexeme += c       

        #Identificador
        if search == 0 and c.islower():
            search = 3
            index = cur_index
            lexeme += c
        elif search == 3 and not c.isupper() and not c.islower():
            if lexeme == 'se' and c == ' ':
                lexeme += c
            elif lexeme == 'se nao' and c == ' ':
                lexeme += c
            elif lexeme == 'se nao ' and c != 's':
                lexeme = lexeme[:-1]
                inserirToken(tokens, groups[3], index, line, lexeme)
                search = 0
                lexeme = ''
            elif lexeme == 'se ' and c != 'n':
                lexeme = lexeme[:-1]
                inserirToken(tokens, groups[3], index, line, lexeme)
                search = 0
                lexeme = ''
            else:

                inserirToken(tokens, groups[3], index, line, lexeme)
                search = 0
                lexeme = ''
        elif search == 3:
            lexeme += c            

        if saving_comment:
            if c != '\n':
                lexeme += c
            else:
                saving_comment = False

                inserirToken(tokens, groups[1], index, line, lexeme)
                search = 0
                lexeme = ''
        
        #atribuicao
        if c == ':':
            if search == 5:
                search = 0
                lexeme += c

                inserirToken(tokens, groups[5], index, line, lexeme)
                lexeme = ''
                inserted_delimiter = True
            elif search == 0:
                index = cur_index
                search = 5
                lexeme += c

        #diferente
        if c == '!' and search == 0:
            index = cur_index
            search = 8
            lexeme += c
        if search == 8 and c == '=':
            search = 0
            lexeme += c
            inserirToken(tokens, groups[8], index, line, lexeme)
            lexeme = ''
            inserted_delimiter = True



        if c in operators and search != 8 and not inserted_delimiter:
            inserirToken(tokens, operators[c], cur_index, line, c)
        if c in delimiter and search != 5 and not inserted_delimiter:
            inserirToken(tokens, delimiter[c], cur_index, line, c)
        if search == 0 and c not in operators and c not in delimiter and c != ' ' and c != '\n' and c != "'":
            search = 0
            inserirToken(tokens, groups[9], cur_index, line, c)
            inserirErro(erros, cur_index, line, c)
            lexeme = ''
        if c == '\n':
            inserirToken(tokens, groups[2], cur_index, line, '\n')
            line += 1
            cur_index = 0
        else:
            cur_index += 1

    return {"tokens":tokens,"erros":erros}

def inserirToken(tokens, grupo, indice, linha, texto):
    global reservado

    if texto in reservado:
        grupo = "reservado"

    obj = {
        "grupo": grupo,
        "texto": texto,
        "local": {
            "linha": linha,
            "indice": indice,
        }
    }

    tokens.append(obj)

def inserirErro(erros, indice, linha, texto):

    obj = {
        "texto": "simbolo, " + texto + ", desconhecido",
        "local": {
            "linha": linha,
            "indice": indice,
        }
    }

    erros.append(obj)

# ALERTA: Nao modificar o codigo fonte apos esse aviso

def testaAnalisadorLexico(programa, teste):
  # Caso o resultado nao seja igual ao teste
  # ambos sao mostrados e a execucao termina  
  resultado = json.dumps(analisadorLexico(programa), indent=2)
  teste = json.dumps(teste, indent=2)
  if resultado != teste:
    # Mostra o teste e o resultado lado a lado  
    resultadoLinhas = resultado.split('\n')
    testeLinhas = teste.split('\n')
    if len(resultadoLinhas) > len(testeLinhas):
      testeLinhas.extend(
        [' '] * (len(resultadoLinhas)-len(testeLinhas))
      )
    elif len(resultadoLinhas) < len(testeLinhas):
      resultadoLinhas.extend(
        [' '] * (len(testeLinhas)-len(resultadoLinhas))
      )
    linhasEmPares = enumerate(zip(testeLinhas, resultadoLinhas))
    maiorTextoNaLista = str(len(max(testeLinhas, key=len)))
    maiorIndice = str(len(str(len(testeLinhas))))
    titule = '{:<'+maiorIndice+'} + {:<'+maiorTextoNaLista+'} + {}'
    objeto = '{:<'+maiorIndice+'} | {:<'+maiorTextoNaLista+'} | {}'
    print(titule.format('', 'teste', 'resultado'))
    print(objeto.format('', '', ''))
    for indice, (esquerda, direita) in linhasEmPares:
      print(objeto.format(indice, esquerda, direita))
    # Termina a execucao
    print("\n): falha :(")
    quit()

# Programa que passdo para a funcao analisadorLexico
programa = """-- funcao inicial

inicio:Funcao(valor:Logica,item:Texto):Numero::{
}

tiposDeVariaveis:Funcao::{
  textoVar:Texto::'#'exemplo##'
  numeroVar:Numero::1234
  logicoVar:Logico::Sim
}

tiposDeFluxoDeControle:Funcao:Logico::{
  resultado:Logico::Nao

  se(1 = 2){
    resultado::Nao
  } se nao se('a' != 'a'){
    resultado::Nao
  } se nao @ {
    resultado::Sim
  }

  contador:Numero::0
  enquanto(contador < 10){
    contador::contador + 'a'
  }

  retorna resultado
}"""

# Resultado esperado da execucao da funcao analisadorLexico
# passando paea ela o programa anterior
teste = {
  "tokens":[
    # Comentario    
    {
      "grupo":"comentario", "texto": "-- funcao inicial", 
      "local":{"linha":1,"indice":0}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":1,"indice":17}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":2,"indice":0}
    },
    # Funcao inicio
    {
      "grupo":"identificador", "texto": "inicio", 
      "local":{"linha":3,"indice":0}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":3,"indice":6}
    },
    {
      "grupo":"reservado", "texto": "Funcao", 
      "local":{"linha":3,"indice":7}
    },
    {
      "grupo":"abre-parenteses", "texto": "(", 
      "local":{"linha":3,"indice":13}
    },
    {
      "grupo":"identificador", "texto": "valor", 
      "local":{"linha":3,"indice":14}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":3,"indice":19}
    },
    {
      "grupo":"reservado", "texto": "Logica", 
      "local":{"linha":3,"indice":20}
    },
    {
      "grupo":"virgula", "texto": ",", 
      "local":{"linha":3,"indice":26}
    },
    {
      "grupo":"identificador", "texto": "item", 
      "local":{"linha":3,"indice":27}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":3,"indice":31}
    },
    {
      "grupo":"reservado", "texto": "Texto", 
      "local":{"linha":3,"indice":32}
    },
    {
      "grupo":"fecha-parenteses", "texto": ")", 
      "local":{"linha":3,"indice":37}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":3,"indice":38}
    },
    {
      "grupo":"reservado", "texto": "Numero", 
      "local":{"linha":3,"indice":39}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":3,"indice":45}
    },
    {
      "grupo":"abre-chaves", "texto": "{", 
      "local":{"linha":3,"indice":47}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":3,"indice":48}
    },
    {
      "grupo":"fecha-chaves", "texto": "}", 
      "local":{"linha":4,"indice":0}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":4,"indice":1}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":5,"indice":0}
    },
    # Funcao tiposDeVariaveis
    {
      "grupo":"identificador", "texto": "tiposDeVariaveis", 
      "local":{"linha":6,"indice":0}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":6,"indice":16}
    },
    {
      "grupo":"reservado", "texto": "Funcao", 
      "local":{"linha":6,"indice":17}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":6,"indice":23}
    },
    {
      "grupo":"abre-chaves", "texto": "{", 
      "local":{"linha":6,"indice":25}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":6,"indice":26}
    },
    # textoVar:Texto::'#'exemplo##'
    {
      "grupo":"identificador", "texto": "textoVar", 
      "local":{"linha":7,"indice":2}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":7,"indice":10}
    },
    {
      "grupo":"reservado", "texto": "Texto", 
      "local":{"linha":7,"indice":11}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":7,"indice":16}
    },
    {
      "grupo":"texto", "texto": "'#'exemplo##'", 
      "local":{"linha":7,"indice":18}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":7,"indice":31}
    },
    # numeroVar:Numero::1234
    {
      "grupo":"identificador", "texto": "numeroVar", 
      "local":{"linha":8,"indice":2}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":8,"indice":11}
    },
    {
      "grupo":"reservado", "texto": "Numero", 
      "local":{"linha":8,"indice":12}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":8,"indice":18}
    },
    {
      "grupo":"numero", "texto": "1234", 
      "local":{"linha":8,"indice":20}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":8,"indice":24}
    },
    # logicoVar:Logico::Sim
    {
      "grupo":"identificador", "texto": "logicoVar", 
      "local":{"linha":9,"indice":2}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":9,"indice":11}
    },
    {
      "grupo":"reservado", "texto": "Logico", 
      "local":{"linha":9,"indice":12}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":9,"indice":18}
    },
    {
      "grupo":"logico", "texto": "Sim", 
      "local":{"linha":9,"indice":20}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":9,"indice":23}
    },
    # Fecha Funcao
    {
      "grupo":"fecha-chaves", "texto": "}", 
      "local":{"linha":10,"indice":0}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":10,"indice":1}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":11,"indice":0}
    },
    # Funcao tiposDeFluxoDeControle
    {
      "grupo":"identificador", "texto": "tiposDeFluxoDeControle", 
      "local":{"linha":12,"indice":0}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":12,"indice":22}
    },
    {
      "grupo":"reservado", "texto": "Funcao", 
      "local":{"linha":12,"indice":23}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":12,"indice":29}
    },
    {
      "grupo":"reservado", "texto": "Logico", 
      "local":{"linha":12,"indice":30}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":12,"indice":36}
    },
    {
      "grupo":"abre-chaves", "texto": "{", 
      "local":{"linha":12,"indice":38}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":12,"indice":39}
    },
    # resultado:Logico::Nao
    {
      "grupo":"identificador", "texto": "resultado", 
      "local":{"linha":13,"indice":2}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":13,"indice":11}
    },
    {
      "grupo":"reservado", "texto": "Logico", 
      "local":{"linha":13,"indice":12}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":13,"indice":18}
    },
    {
      "grupo":"logico", "texto": "Nao", 
      "local":{"linha":13,"indice":20}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":13,"indice":23}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":14,"indice":0}
    },
    # se(1 = 2){
    {
      "grupo":"reservado", "texto": "se", 
      "local":{"linha":15,"indice":2}
    },
    {
      "grupo":"abre-parenteses", "texto": "(", 
      "local":{"linha":15,"indice":4}
    },
    {
      "grupo":"numero", "texto": "1", 
      "local":{"linha":15,"indice":5}
    },
    {
      "grupo":"operador-igual", "texto": "=", 
      "local":{"linha":15,"indice":7}
    },
    {
      "grupo":"numero", "texto": "2", 
      "local":{"linha":15,"indice":9}
    },
    {
      "grupo":"fecha-parenteses", "texto": ")", 
      "local":{"linha":15,"indice":10}
    },
    {
      "grupo":"abre-chaves", "texto": "{",
      "local":{"linha":15,"indice":11}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":15,"indice":12}
    },
    {
      "grupo":"identificador", "texto": "resultado", 
      "local":{"linha":16,"indice":4}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":16,"indice":13}
    },
    {
      "grupo":"logico", "texto": "Nao", 
      "local":{"linha":16,"indice":15}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":16,"indice":18}
    },
    # } se nao se('a' != 'a'){
    {
      "grupo":"fecha-chaves", "texto": "}",
      "local":{"linha":17,"indice":2}
    },
    {
      "grupo":"reservado", "texto": "se nao se", 
      "local":{"linha":17,"indice":4}
    },
    {
      "grupo":"abre-parenteses", "texto": "(", 
      "local":{"linha":17,"indice":13}
    },
    {
      "grupo":"texto", "texto": "'a'", 
      "local":{"linha":17,"indice":14}
    },
    {
      "grupo":"operador-diferente", "texto": "!=", 
      "local":{"linha":17,"indice":18}
    },
    {
      "grupo":"texto", "texto": "'a'", 
      "local":{"linha":17,"indice":21}
    },
    {
      "grupo":"fecha-parenteses", "texto": ")", 
      "local":{"linha":17,"indice":24}
    },
    {
      "grupo":"abre-chaves", "texto": "{",
      "local":{"linha":17,"indice":25}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":17,"indice":26}
    },
    {
      "grupo":"identificador", "texto": "resultado", 
      "local":{"linha":18,"indice":4}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":18,"indice":13}
    },
    {
      "grupo":"logico", "texto": "Nao", 
      "local":{"linha":18,"indice":15}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":18,"indice":18}
    },
    # } se nao @ {
    {
      "grupo":"fecha-chaves", "texto": "}",
      "local":{"linha":19,"indice":2}
    },
    {
      "grupo":"reservado", "texto": "se nao", 
      "local":{"linha":19,"indice":4}
    },
    {
      "grupo":"desconhecido", "texto": "@", 
      "local":{"linha":19,"indice":11}
    },
    {
      "grupo":"abre-chaves", "texto": "{",
      "local":{"linha":19,"indice":13}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":19,"indice":14}
    },
    {
      "grupo":"identificador", "texto": "resultado", 
      "local":{"linha":20,"indice":4}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":20,"indice":13}
    },
    {
      "grupo":"logico", "texto": "Sim", 
      "local":{"linha":20,"indice":15}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":20,"indice":18}
    },
    {
      "grupo":"fecha-chaves", "texto": "}", 
      "local":{"linha":21,"indice":2}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":21,"indice":3}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":22,"indice":0}
    },
    # contador:Numero::0
    {
      "grupo":"identificador", "texto": "contador", 
      "local":{"linha":23,"indice":2}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":23,"indice":10}
    },
    {
      "grupo":"reservado", "texto": "Numero", 
      "local":{"linha":23,"indice":11}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":23,"indice":17}
    },
    {
      "grupo":"numero", "texto": "0", 
      "local":{"linha":23,"indice":19}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":23,"indice":20}
    },
    # enquanto(contador < 10){
    {
      "grupo":"reservado", "texto": "enquanto", 
      "local":{"linha":24,"indice":2}
    },
    {
      "grupo":"abre-parenteses", "texto": "(", 
      "local":{"linha":24,"indice":10}
    },
    {
      "grupo":"identificador", "texto": "contador", 
      "local":{"linha":24,"indice":11}
    },
    {
      "grupo":"operador-menor", "texto": "<", 
      "local":{"linha":24,"indice":20}
    },
    {
      "grupo":"numero", "texto": "10", 
      "local":{"linha":24,"indice":22}
    },
    {
      "grupo":"fecha-parenteses", "texto": ")", 
      "local":{"linha":24,"indice":24}
    },
    {
      "grupo":"abre-chaves", "texto": "{",
      "local":{"linha":24,"indice":25}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":24,"indice":26}
    },
    {
      "grupo":"identificador", "texto": "contador", 
      "local":{"linha":25,"indice":4}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":25,"indice":12}
    },
    {
      "grupo":"identificador", "texto": "contador", 
      "local":{"linha":25,"indice":14}
    },
    {
      "grupo":"operador-mais", "texto": "+", 
      "local":{"linha":25,"indice":23}
    },
    {
      "grupo":"texto", "texto": "'a'", 
      "local":{"linha":25,"indice":25}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":25,"indice":28}
    },
    {
      "grupo":"fecha-chaves", "texto": "}", 
      "local":{"linha":26,"indice":2}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":26,"indice":3}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":27,"indice":0}
    },
    # Fecha Funcao
    {
      "grupo":"reservado", "texto": "retorna", 
      "local":{"linha":28,"indice":2}
    },    
    {
      "grupo":"identificador", "texto": "resultado", 
      "local":{"linha":28,"indice":10}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":28,"indice":19}
    },
    {
      "grupo":"fecha-chaves", "texto": "}", 
      "local":{"linha":29,"indice":0}
    }
  ], "erros":[
    {
      "texto":"simbolo, @, desconhecido",
      "local":{"linha":19,"indice":11}
    }
  ]
}

# Execucao do teste que valida a funcao analisadorLexico
testaAnalisadorLexico(programa, teste)
print("(: sucesso :)")