# To-Do de Livros com FastAPI

![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green.svg)

## Sobre o Projeto

Este projeto é uma API de gerenciamento de tarefas para livros, permitindo que os usuários adicionem, editem, removam e listem livros em uma lista de leitura. A API foi desenvolvida utilizando o FastAPI para fornecer uma solução eficiente e moderna para controle de leituras.

## Funcionalidades
- Criar uma nova tarefa de leitura
- Listar todas as tarefas
- Atualizar uma tarefa existente
- Remover uma tarefa
- Suporte a documentação automática com Swagger UI e Redoc

## Tecnologias Utilizadas
- Python 3.x
- FastAPI
- Uvicorn

## Como Executar

### Pré-requisitos
Certifique-se de ter o Python instalado em sua máquina.

### Execução do Projeto
1. Clone este repositório:
2. Acesse o diretório do projeto:
3. Execute o servidor FastAPI:
4. Acesse a API via navegador ou Postman:
   - Documentação Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Documentação Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Exemplos de Uso

### Criar um novo livro para leitura
```json
POST /books
{
  "title": "O Senhor dos Anéis",
  "author": "J.R.R. Tolkien",
  "status": "pendente"
}
```

### Listar todos os livros
```json
GET /books
```

### Atualizar o status de um livro
```json
PUT /books/{id}
{
  "status": "concluído"
}
```

### Remover um livro
```json
DELETE /books/{id}
```

## Contribuição

Sinta-se à vontade para contribuir! Para isso:
1. Faça um fork do repositório
2. Crie uma branch com sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas modificações (`git commit -m 'Adicionando nova funcionalidade'`)
4. Envie para o repositório remoto (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Projeto desenvolvido para gerenciar listas de leitura utilizando FastAPI.

