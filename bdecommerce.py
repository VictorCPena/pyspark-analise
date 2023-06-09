import psycopg2
import random
from datetime import datetime
from config import host, database, user, password

conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Categorias (
        ID SERIAL PRIMARY KEY,
        Nome VARCHAR(255)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Subcategorias (
        ID SERIAL PRIMARY KEY,
        IDCategoria INTEGER REFERENCES Categorias(ID),
        Nome VARCHAR(255)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Produtos (
        ID SERIAL PRIMARY KEY,
        Nome VARCHAR(255),
        Descricao TEXT,
        Preco NUMERIC(10, 2),
        IDCategoria INTEGER REFERENCES Categorias(ID),
        IDSubcategoria INTEGER REFERENCES Subcategorias(ID)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clientes (
        ID SERIAL PRIMARY KEY,
        Nome VARCHAR(255),
        Endereco TEXT,
        Email VARCHAR(255),
        Senha VARCHAR(255)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pedidos (
        ID SERIAL PRIMARY KEY,
        IDCliente INTEGER REFERENCES Clientes(ID),
        DataHora TIMESTAMP,
        Total NUMERIC(10, 2)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ItensPedido (
        ID SERIAL PRIMARY KEY,
        IDPedido INTEGER REFERENCES Pedidos(ID),
        IDProduto INTEGER REFERENCES Produtos(ID),
        Quantidade INTEGER,
        PrecoUnitario NUMERIC(10, 2)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS CarrinhosCompras (
        ID SERIAL PRIMARY KEY,
        IDCliente INTEGER REFERENCES Clientes(ID)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ItensCarrinho (
        ID SERIAL PRIMARY KEY,
        IDCarrinho INTEGER REFERENCES CarrinhosCompras(ID),
        IDProduto INTEGER REFERENCES Produtos(ID),
        Quantidade INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS AvaliacoesProdutos (
        ID SERIAL PRIMARY KEY,
        IDProduto INTEGER REFERENCES Produtos(ID),
        IDCliente INTEGER REFERENCES Clientes(ID),
        Pontuacao INTEGER,
        Comentario TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS InformacoesPagamento (
        ID SERIAL PRIMARY KEY,
        IDPedido INTEGER REFERENCES Pedidos(ID),
        MetodoPagamento VARCHAR(255),
        ValorPagamento NUMERIC(10, 2),
        DataHoraPagamento TIMESTAMP
    )
''')

categorias = ["Roupas", "Calçados", "Eletrônicos", "Livros", "Tecnologia"]
subcategorias = [
    ["Vestidos", "Camisas", "Calças", "Saias", "Blusas"],
    ["Tênis", "Sapatos", "Sandálias", "Botas"],
    ["Celulares", "Tablets", "Notebooks", "Fones de Ouvido", "Smartwatches"],
    ["Romance", "Ficção Científica", "Biografia", "Autoajuda"],
    ["Gadgets", "Acessórios", "Periféricos", "Componentes"]
]

produtos_existentes = [
    ("Vestido Floral", "Vestido estampado floral", 59.99, 1, 1),
    ("Camisa Xadrez", "Camisa xadrez masculina", 39.99, 1, 2),
    ("Calça Jeans", "Calça jeans masculina", 79.99, 1, 3),
    ("Tênis Esportivo", "Tênis esportivo para corrida", 99.99, 2, 1),
    ("Celular Smartphone", "Smartphone com tela Full HD", 699.99, 3, 1),
    ("Mouse Sem Fio", "Mouse sem fio com tecnologia Bluetooth", 19.99, 5, 1),
    ("Saia Midi", "Saia midi estampada", 39.99, 1, 4),
    ("Bota de Couro", "Bota de couro feminina", 129.99, 2, 4),
    ("Notebook", "Notebook com processador Intel Core i5", 699.99, 3, 3),
    ("Teclado Mecânico", "Teclado mecânico para jogos", 79.99, 2, 5),
    ("Camiseta Listrada", "Camiseta listrada de algodão", 29.99, 1, 5),
    ("Tênis Casual", "Tênis casual em couro sintético", 49.99, 2, 2),
    ("Fone de Ouvido Bluetooth", "Fone de ouvido Bluetooth com cancelamento de ruído", 89.99, 3, 4),
    ("Livro de Suspense", "Livro de suspense e mistério", 19.99, 4, 1),
    ("Smartwatch Fitness", "Smartwatch com monitor de atividades físicas", 149.99, 3, 5),
    ("Câmera de Segurança", "Câmera de segurança com gravação em HD", 59.99, 5, 6),
    ("Blusa de Tricô", "Blusa de tricô feminina", 49.99, 1, 6),
    ("Sapato Social", "Sapato social masculino", 89.99, 2, 3),
    ("Headset Gamer", "Headset gamer com som surround", 69.99, 3, 2),
    ("Livro de Ficção Científica", "Livro de ficção científica", 24.99, 4, 2),
    ("Caixa de Som Bluetooth", "Caixa de som portátil com conexão Bluetooth", 39.99, 5, 3),
    ("Camiseta Estampada", "Camiseta estampada de algodão", 29.99, 1, 7),
    ("Sapatilha Feminina", "Sapatilha feminina de couro sintético", 39.99, 2, 1),
    ("Smartphone de Última Geração", "Smartphone com tecnologia avançada", 999.99, 3, 1),
    ("Livro de Biografia", "Livro de biografia de uma personalidade famosa", 29.99, 4, 3),
    ("Cabo USB", "Cabo USB para carregamento rápido", 9.99, 5, 4),
    ("Blazer Masculino", "Blazer masculino de tecido fino", 79.99, 1, 8),
    ("Sandália Rasteira", "Sandália rasteira feminina", 29.99, 2, 2),
    ("Tablet", "Tablet com tela de alta definição", 199.99, 3, 2),
    ("Livro de Autoajuda", "Livro de autoajuda para o sucesso pessoal", 19.99, 4, 4),
    ("Placa de Vídeo", "Placa de vídeo para jogos de última geração", 299.99, 5, 5)
]


for categoria in categorias:
    cursor.execute("INSERT INTO Categorias (Nome) VALUES (%s)", (categoria,))
    conn.commit()

for categoria_id, subcategoria_lista in enumerate(subcategorias, start=1):
    for subcategoria in subcategoria_lista:
        cursor.execute("INSERT INTO Subcategorias (IDCategoria, Nome) VALUES (%s, %s)", (categoria_id, subcategoria))
        conn.commit()

for _ in range(450000):
    produto = random.choice(produtos_existentes)
    nome, descricao, preco, categoria_id, subcategoria_id = produto
    cursor.execute(
        "INSERT INTO Produtos (Nome, Descricao, Preco, IDCategoria, IDSubcategoria) VALUES (%s, %s, %s, %s, %s)",
        (nome, descricao, preco, categoria_id, subcategoria_id))
    conn.commit()

nomes = ["Ana Luiza", "Bianca Maria", "Carla Fernanda", "Diego Rafael", "Eduarda Beatriz", "Fernando Henrique",
         "Gabriel Antônio", "Henrique Eduardo", "Isabela Cristina", "João Lucas", "Karine Beatriz", "Laura Victoria",
         "Ana Julia", "Ana Luiza",
         "Natália Carolina", "Otávio Augusto", "Pedro Henrique", "Quirino José", "Rafaela Fernanda", "Sofia Isabel",
         "Thiago Felipe", "Úrsula Maria", "Valentina Raquel", "William Eduardo", "Xavier Matheus", "Yasmin Vitória",
         "Zoe Juliana", "Maria Gabriela",
         "Ricardo Henrique", "Renata Beatriz", "Paulo André", "Juliana Gabriela", "Amanda", "Bruno", "Cecília",
         "Daniel", "Elisa", "Felipe", "Giovanna", "Henrique", "Isadora", "José", "Karina", "Larissa", "Matheus",
         "Natália", "Otto", "Priscila", "Sara",
         "Quentin", "Roberto", "Samuel", "Thalita", "Ulisses", "Vanessa", "Wagner", "Ximena", "Yasmin", "Zélia",
         "Rafaela", "Ricardo", "Paula", "Júlio", "Ana", "Beatriz", "Carlos", "Diego", "Eduarda", "Fernanda", "Gabriel",
         "Hugo", "Isabel", "João","Karine", "Lucas", "Mariana", "Nathalia", "Otávio", "Pedro", "Quirino", "Rafael",
         "Sofia", "Thiago", "Ursula","Valentina", "William", "Xavier", "Yuri", "Zoe", "Ricardo", "Renata", "Paulo",
         "Juliana", "Victor", "Vinicius","Gabriela"]

sobrenomes = ["Silva", "Souza", "Oliveira", "Pereira", "Costa", "Ferreira", "Rodrigues", "Almeida", "Lima", "Melo",
              "Garcia", "Martins", "Gomes", "Ribeiro", "Mendes", "Carvalho", "Coelho", "Moura", "Santos", "Nascimento",
              "Fernandes", "Marques", "Araújo", "Cardoso", "Barbosa", "Freitas", "Pena", "Cavalcante", "Ramos",
              "Basílio","Pinto", "Vasco", "Gama", "Vasconcelos", "Cunha", "Amaral", "Correia", "Dantas", "Leite", "Leal",
              "Magalhães", "Guimarães"]

for _ in range(7500):
    nome = random.choice(nomes)
    sobrenome = random.choice(sobrenomes)
    endereco = "Endereço do cliente"
    email = f"{nome.lower()}.{sobrenome.lower()}@exemplo.com"
    senha = "senha123"

    cursor.execute("INSERT INTO Clientes (Nome, Endereco, Email, Senha) VALUES (%s, %s, %s, %s)",
                   (f"{nome} {sobrenome}", endereco, email, senha))
    conn.commit()

cursor.execute("SELECT ID FROM Clientes")
existing_ids = [row[0] for row in cursor.fetchall()]

if existing_ids:
    for _ in range(750000):
        id_cliente = random.choice(existing_ids)
        data_hora = datetime.now()
        total = random.uniform(1, 400000)

        cursor.execute("INSERT INTO Pedidos (IDCliente, DataHora, Total) VALUES (%s, %s, %s)",
                       (id_cliente, data_hora, total))
        conn.commit()


# Inserir um pedido
cursor.execute('''
    INSERT INTO Pedidos (IDCliente, DataHora, Total)
    VALUES (%s, %s, %s)
    RETURNING ID
''', (id_cliente, data_hora, total))

pedido_id = cursor.fetchone()[0]  # Obter o ID do pedido inserido

for _ in range(350000):
    id_produto = random.randint(1, len(produtos_existentes))
    quantidade = random.randint(1, 5)
    preco_unitario = random.uniform(10, 1000)

    cursor.execute('''
        INSERT INTO ItensPedido (IDPedido, IDProduto, Quantidade, PrecoUnitario)
        VALUES (%s, %s, %s, %s)
    ''', (pedido_id, id_produto, quantidade, preco_unitario))

conn.commit()

for _ in range(750000):
    id_cliente = random.randint(1, 750000)

    cursor.execute("SELECT COUNT(*) FROM Clientes WHERE ID = %s", (id_cliente,))
    count = cursor.fetchone()[0]

    if count > 0:
        cursor.execute("INSERT INTO CarrinhosCompras (IDCliente) VALUES (%s)", (id_cliente,))
        conn.commit()

for _ in range(750000):
    id_carrinho = random.randint(1, 750000)
    id_produto = random.randint(1, len(produtos_existentes))
    quantidade = random.randint(1, 9)

    cursor.execute("SELECT COUNT(*) FROM CarrinhosCompras WHERE ID = %s", (id_carrinho,))
    count = cursor.fetchone()[0]

    if count > 0:
        cursor.execute("INSERT INTO ItensCarrinho (IDCarrinho, IDProduto, Quantidade) VALUES (%s, %s, %s)",
                       (id_carrinho, id_produto, quantidade))
        conn.commit()


for _ in range(250000):
    id_produto = random.randint(1, len(produtos_existentes))
    id_cliente = random.randint(1, 750000)
    pontuacao = random.randint(1, 5)
    comentario = "Ótimo produto!"

    cursor.execute("SELECT COUNT(*) FROM Produtos WHERE ID = %s", (id_produto,))
    count_produto = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Clientes WHERE ID = %s", (id_cliente,))
    count_cliente = cursor.fetchone()[0]

    if count_produto > 0 and count_cliente > 0:
        cursor.execute(
            "INSERT INTO AvaliacoesProdutos (IDProduto, IDCliente, Pontuacao, Comentario) VALUES (%s, %s, %s, %s)",
            (id_produto, id_cliente, pontuacao, comentario))
        conn.commit()


for _ in range(275000):
    id_pedido = random.randint(1, 350000)
    metodo_pagamento = random.choice(["Cartão de Crédito", "Transferência Bancária", "Boleto Bancário"])
    valor_pagamento = random.uniform(1, 3000)
    data_hora_pagamento = datetime.now()

    cursor.execute("SELECT COUNT(*) FROM Pedidos WHERE ID = %s", (id_pedido,))
    count_pedido = cursor.fetchone()[0]

    if count_pedido > 0:
        cursor.execute(
            "INSERT INTO InformacoesPagamento (IDPedido, MetodoPagamento, ValorPagamento, DataHoraPagamento) VALUES (%s, %s, %s, %s)",
            (id_pedido, metodo_pagamento, valor_pagamento, data_hora_pagamento))
        conn.commit()

conn.commit()
conn.close()

print('operação feita!')