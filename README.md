# 🕒 Controle de Ponto em Python 

Um aplicativo simples de controle de ponto e produtividade com interface leve, flutuante e funcional para registrar entradas, pausas, reuniões, feedbacks e horários de almoço. Ideal para ambientes corporativos ou equipes remotas.

---

## 🚀 Funcionalidades

- Registro de **entrada** e **saída**.
- Controle de até **duas pausas** por jornada.
- Registro de **almoço**, **reuniões**, **feedbacks** e **indisponibilidade**.
- Interface compacta, **transparente e sempre visível** na tela.
- Temporizador ao vivo por status.
- Alerta automático de **tempo excedido** para almoço e pausas.
- Geração de **relatório detalhado** com porcentagem de tempo por atividade.
- **Exportação de logs** em `.txt`.
- Salvamento e carregamento automático de histórico em `.json`.

---

## 🖼️ Captura de Tela

![image](https://github.com/user-attachments/assets/6e07e145-36ee-4385-868f-c20832102740)


---

## 🛠️ Tecnologias Utilizadas

- [Python 3.10+](https://www.python.org/)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Tkinter (nativo do Python)
- JSON (armazenamento dos logs)
- `datetime` e `timedelta` para controle de tempo

---

## 📦 Instalação

1. Clone o repositório:

git clone https://github.com/seu-usuario/controle-ponto-python.git
cd controle-ponto-python

2. Crie um ambiente virtual (opcional):

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Instale as dependências:

pip install customtkinter

4. Execute o programa:

python main.py

🧠 Como Usar
Inicie clicando em "Entrada".

Use os botões de Pausa, Almoço, Reunião, Feedback e Indisponível conforme necessário.

Clique em "Logs" para visualizar um relatório completo e exportar os dados.

📁 Estrutura dos Arquivos
main.py: Código principal da aplicação.

logs_ponto.json: Armazena logs persistentes da sessão.

logs_ponto.txt: Arquivo gerado na exportação dos logs.

🔐 Observações
Os dados são armazenados localmente no mesmo diretório do script.

O sistema não faz controle por usuário. Cada instância do app equivale a um colaborador.

Ideal para uso em estações individuais ou para fins de acompanhamento pessoal.

📜 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

🤝 Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, enviar pull requests ou sugerir melhorias.
