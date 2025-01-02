# Documentação do Sistema de Controle de Ponto 🌟📋✨

Este sistema é um aplicativo web desenvolvido em Django para gestão de controle de ponto de funcionários. Abaixo estão descritas as funcionalidades principais, estrutura do projeto e instruções de uso. 🎯🚀📜

---

## Funcionalidades Principais 🎉📂✅

1. **Gestão de Empresas**:
   - Listagem de empresas.
   - Criação de novas empresas.
   - Atualização de informações das empresas.

2. **Gestão de Funcionários**:
   - Listagem de funcionários associados a uma empresa.
   - Registro de novos funcionários com vinculação a uma empresa.
   - Atualização de dados dos funcionários.

3. **Controle de Ponto**:
   - Registro de entradas, intervalos e saídas de funcionários.
   - Listagem e filtragem de pontos por funcionário e data.
   - Atualização de registros de ponto existentes.

4. **Autenticação de Usuários**:
   - Registro de novos usuários.
   - Login e logout.
   - Proteção de rotas por autenticação.

---

## Estrutura do Projeto 🏗️📚🔍

### Views

As views são organizadas para atender cada funcionalidade principal:

#### **Autenticação** 🔑🛡️👤
- `registrar_usuario(request)`: Registra novos usuários.
- `login_usuario(request)`: Realiza o login de usuários.
- `logout_usuario(request)`: Realiza o logout de usuários autenticados.

#### **Empresas** 🏢📋✏️
- `EmpresaListView`: Exibe a lista de empresas.
- `EmpresaCreateView`: Permite criar novas empresas.
- `EmpresaUpdateView`: Permite atualizar dados de empresas existentes.

#### **Funcionários** 👥📝🛠️
- `FuncionarioListView`: Exibe a lista de funcionários.
- `FuncionarioCreateView`: Permite criar novos funcionários.
- `FuncionarioUpdateView`: Permite atualizar dados de funcionários.

#### **Pontos** 📊⏰✅
- `PontoListView`: Exibe e filtra registros de ponto.
- `PontoCreateView`: Cria novos registros de ponto.
- `PontoUpdateView`: Atualiza registros de ponto existentes.

---


### Requisitos:
   - Python 3.8+
   - Django 3.2+
   - PostgreSQL
   - Docker e Docker Compose (opcional para ambiente conteinerizado)

### Passo a passo:

1. **Configuração do Ambiente ⚙️🖥️📦**

Clonar o Repositório Certifique-se de clonar o repositório para sua máquina local:
```
   git clone https://github.com/TImoteoVieira/ponto_m2.git
   cd ponto_m2
```
Criar um Ambiente Virtual Crie um ambiente virtual para isolar as dependências do projeto:
```
python3 -m venv venv
```

Linux/MacOS:
```
source venv/bin/activate
```



Windows (cmd):
```
venv\Scripts\activate
```

Instalar Dependências Com o ambiente virtual ativado, instale as dependências listadas no arquivo requirements.txt:

```
pip install -r requirements.txt
```

2. **Configuração do Banco de Dados**:
   Um arquivo `docker-compose.yml` é fornecido para facilitar a configuração do PostgreSQL. Certifique-se de que o Docker esteja instalado e em execução. 🐳📂💾

   Inicie o contêiner:
   ```bash
   docker compose up -d --build 
   ```

3. **Migrações e Seeds do Banco**:
   Aplique as migrações para criar as tabelas:
   ```bash
   python3 manage.py migrate
   ```
   
   Aplique os Seeds para criar a empresa M2:
   ```
   python3 manage.py seed
   ```

4. **Execução do Servidor**:
   Inicie o servidor de desenvolvimento:
   ```bash
   python3 manage.py runserver
   ```

---

## Testes Automatizados 🧪✅📊

Os testes são escritos para cobrir as principais funcionalidades:

1. **Localização dos Testes**:
   - `ponto/tests/auth_views.py`: Testes de autenticação.
   - `ponto/tests/empresa_views.py`: Testes relacionados a empresas.
   - `ponto/tests/funcionario_views.py`: Testes relacionados a funcionários.
   - `ponto/tests/ponto_views.py`: Testes de controle de ponto.

2. **Executando os Testes**:
   Utilize o `pytest` para executar todos os testes:
   ```bash
   pytest
   ```
---

## Contribuições 🤝✨🌟

Sinta-se à vontade para contribuir com este projeto. Certifique-se de seguir estas etapas:

1. Faça um fork do repositório.
2. Crie um branch para sua feature/bugfix:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça commit das suas alterações.
4. Envie suas alterações para o branch principal.
5. Abra um pull request.

---

## Contato 📧💬📞

Para dúvidas ou sugestões, entre em contato em [timoteodeveloper@gmail.com]. 🌟✉️📬