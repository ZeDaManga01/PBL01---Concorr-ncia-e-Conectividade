## Introdução
  
  Este sistema permite a compra de passagens aéreas, utilizando um modelo cliente-servidor. O servidor gerencia a disponibilidade dos trechos e processa as solicitações dos clientes, enquanto os clientes interagem com o sistema para consultar e comprar passagens. O sistema aprensenta limitações a serem tratadas em versões futuras, como a impossibilidade de realizar duas confirmações ao mesmo tempo, retomar conexão do cliente em caso de desconexão, retornar a etapa pre-desconexão e além disso de ter uma estrutura simplificada e sem funcionalidades adicionais. Estando totalmente direcionado a um processo basico de consulta e Confirmação de compra
## Arquitetura da Solução
### Componentes
#### Servidor
- Função: Gerencia as conexões com os clientes, processa as solicitações de compra e atualiza a disponibilidade dos trechos de voo.
- Tecnologias: Socket TCP, threading para suporte a múltiplas conexões simultâneas.
- Arquivos Utilizados: Voos.json (contém a disponibilidade dos trechos).
#### Cliente
- Função: Conecta-se ao servidor, envia solicitações sobre a disponibilidade dos trechos e gerencia o processo de compra.
- Tecnologias: Socket TCP.
- Entrada do Usuário: Informações sobre trechos de voo e decisão de compra.
## Paradigma de Comunicação
  Foi utilizado o paradigma de stateless na parte relacionada ao processo de compra. O servidor mantém o estado da disponibilidade dos trechos de voo e atualiza essas informações com base nas ações dos clientes. Foi tomada essa decisão para garantir que a disponibilidade das passagens fosse precisa e quer as compras fossem processadas corretamente ao longo do processo. 
## Protocolo de Comunicação
O protocolo de comunicação estabelecido é baseado no uso de mensagens de texto enviadas via sockets TCP, que são codificadas no envio e decodificadas no seu recebimento. A seguir estão as mensagens a serem transmitidas e a ordem das comunicações entre o cliente e o servidor:

  1 - Cliente para Servidor:
  - Envio da solicitação de disponibilidade no formato origem > destino.
    
  2 - Servidor para Cliente:
  - Resposta sobre a disponibilidade do trecho (True ou False).
  
  3 - Cliente para Servidor:
  - Se o trecho estiver disponível, o cliente decide se deseja comprar e envia a resposta (S ou N).
  
  4 - Servidor para Cliente:
  - Confirmação se a compra foi realizada com sucesso (True ou False).
    
## Formatação e Tratamento de Dados
  A formatação dos dados foi feita utilizando texto simples codificado em UTF-8. As mensagens são enviadas e recebidas como strings, facilitando a comunicação entre o cliente e o servidor, devido a impossibilidade de enviar valores booleanos(True ou False) diretamente.

  - Trecho de voo: origem > destino
    
  - Resposta de disponibilidade: True ou False
  
  - Resposta de compra: S ou N
    
## Tratamento de Conexões Simultâneas
  O sistema permite a realização de compras de passagens simultaneamente. O servidor usa threads para lidar com múltiplas conexões simultâneas, permitindo que vários clientes interajam com o servidor ao mesmo tempo. Porém devido ao uso do mutex para tratar de situações de corrida, apenas uma compra pode ser confimada por vez, para que a integridade dos dados não seja afetada por leituras e alterações simultaneas.
### Otimização do Paralelismo
  - Uso de Threads: Cada conexão é tratada em uma thread separada, permitindo que o servidor processe múltiplas requisições simultaneamente.
## Tratamento de Concorrência
  Para gerenciar o acesso simultâneo ao arquivo JSON que contém a disponibilidade dos trechos, o sistema utiliza um mutex (threading.Lock()). Isso garante que apenas uma thread possa ler ou escrever no arquivo por vez, evitando condições de corrida e mantendo a integridade dos dados durante o processo, o que por consequencia acaba por gerar a necessidade de uma solução para caso o cliente simplesmente não responda, o que resultaria em uma espera eterna por parte dos outros clientes conectados. Isso foi solucionado atraves da implementação de um limite de tempo para que a confirmação da compra seja realizada, caso o tempo acabe o cliente é desconectado para que outra compra possa ser confirmada e por sua vez ler e escrever os dados.
## Desempenho e Avaliação
### Mecanismos de Melhoria de Desempenho
  - Threads: Utilização de threads para melhorar a capacidade de resposta e permitir o processamento paralelo das requisições, mas não a sua confirmação.
    
## Confiabilidade da Solução
  O sistema continua funcionando mesmo se um nó (cliente ou servidor) for desconectado e reconectado. No entanto, o estado da compra não é mantido após a desconexão. O sistema não possui funcionalidade para retomar uma compra interrompida, sendo necessario conectar novamente e realizar outra compra.

## Funções do código
### Servidor:
  - info_servidor(): Solicita IP e porta do servidor.
  - iniciar_servidor(): Inicializa e configura o servidor.
  - handle_client(): Gerencia a comunicação com cada cliente.
  - processar_solicitacao(): Verifica e atualiza a disponibilidade dos trechos.
  - aceitar_conexoes(): Aceita e gerencia conexões dos clientes.
  - main(): Função principal para iniciar o servidor.
### Cliente:
  - info_servidor(): Solicita IP e porta do servidor.
  - conetar_servidor(): Conecta ao servidor.
  - enviar_msg(): Envia mensagens ao servidor e recebe respostas.
  - processar_comprar(): Gerencia o processo de compra.
  - handle_interaction(): Loop principal de interação com o servidor.
  - main(): Função principal para iniciar o cliente.

