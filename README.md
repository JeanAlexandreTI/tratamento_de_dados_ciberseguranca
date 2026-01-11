# Tratamento de Incidentes – MySQL + Polars

Este projeto consiste em um script Python voltado para extração, limpeza, padronização e correção de dados de incidentes armazenados em um banco MySQL. A ideia aqui não é só puxar dado e imprimir na tela, mas sim simular um cenário bem real: dados inconsistentes, erros de digitação, status conflitantes e informações faltantes — aquele caos que todo analista já conhece.

O script conecta em um banco MySQL, consulta a tabela incident, transforma os dados usando Polars e aplica regras de negócio para corrigir problemas comuns antes de qualquer análise ou visualização. Em outras palavras: ele arruma a bagunça antes que ela vire dashboard mentiroso.

# Tecnologias utilizadas

O script foi desenvolvido em Python, utilizando algumas bibliotecas bem específicas. O mysql-connector-python é responsável pela conexão com o banco de dados MySQL. O polars entra como motor de processamento de dados, escolhido pela performance e clareza na transformação dos dados. O python-dotenv é usado para carregar variáveis de ambiente, evitando que credenciais sensíveis sejam expostas no código. Por fim, o módulo datetime é usado para lidar com datas inexistentes ou artificiais.

# Estrutura e funcionamento do script

O fluxo do script é simples, direto e sem firula. Primeiro, as variáveis de ambiente são carregadas a partir de um arquivo .env, contendo credenciais do banco de dados como host, usuário, senha e nome do banco. Isso evita o clássico erro de subir senha junto com o projeto — pecado capital no GitHub.

Com as credenciais carregadas, o script estabelece conexão com o MySQL e executa uma consulta SELECT * FROM incident. Os dados retornados não são jogados diretamente em um DataFrame de uma vez; eles são percorridos linha a linha e organizados manualmente em um dicionário. Isso facilita o controle explícito das colunas e evita surpresas caso a ordem dos campos mude no banco.

# Regras de tratamento aplicadas

A partir desse ponto, começa o trabalho sujo — e necessário.

Incidentes com status canceled que possuem data de resolução são incoerentes, então a data de resolução é anulada. Já incidentes marcados como resolved mas sem data de resolução não fazem sentido nenhum, então o status é automaticamente ajustado para in progress. Existe também uma correção pontual de dado incorreto, onde um incidente específico recebe um novo código de ticket fixo, simulando um ajuste manual que frequentemente acontece em bases reais.

Datas nulas no campo resolved_at são substituídas por uma data artificial extremamente antiga (01/01/1800). Isso permite manter consistência de tipo no campo e facilita filtros posteriores sem precisar lidar com NULL o tempo todo.

Depois disso, o script entra na fase de padronização textual. Códigos de ticket, severidade e status são convertidos para letras maiúsculas. Tipos de incidentes passam por correções ortográficas clássicas, como brute-fore virando brute-force e pishing sendo corrigido para phishing. Nada sofisticado, mas extremamente necessário.

Para fechar, registros duplicados são removidos com base no ticket_code, mantendo apenas uma ocorrência por ticket, e os dados são ordenados pelo incident_id.

# Resultado final

Ao final da execução, o script imprime no terminal um DataFrame limpo, padronizado, sem duplicidades óbvias e com regras de negócio aplicadas. Esse dataset já está pronto para ser usado em análises, dashboards ou exportações futuras, sem aquela sensação de “isso aqui tá errado, mas vamos fingir que não vimos”.

A conexão com o banco é encerrada corretamente, evitando vazamento de recurso e mantendo o mínimo de decência técnica.

Variáveis de ambiente necessárias

Para o script funcionar, é obrigatório criar um arquivo .env na raiz do projeto contendo as seguintes variáveis:

HOST=seu_host_mysql
DATABASE=nome_do_banco
USER=usuario_mysql
PASSWORD_SQL=sua_senha


Esse arquivo não deve ser versionado. Coloque-o no .gitignore e durma tranquilo.

# Observações finais

Este script não foi feito para ser genérico ou bonito, foi feito para ser realista. Ele reflete exatamente o tipo de tratamento que acontece quando dados vêm tortos, escritos errado e sem padrão nenhum. É um ótimo ponto de partida para pipelines de limpeza, provas de conceito ou projetos de análise de dados com foco em qualidade da informação.

Se rodou sem erro e os dados fazem sentido, parabéns: você acabou de salvar alguém de tomar decisão baseada em lixo.
