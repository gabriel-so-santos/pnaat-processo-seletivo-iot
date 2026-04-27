# Processo Seletivo – Intensivo Maker | IoT
## Etapa Prática – Sistemas Embarcados

---

### 👤 Identificação 

- **Nome completo:** Gabriel Souza Santos
- **GitHub:** https://github.com/gabriel-so-santos

---

## 1️⃣ Visão Geral da Solução

O projeto consiste em um sistema embarcado simulado para monitoramento de temperatura e umidade utilizando o sensor
DHT22. O sistema permite ao usuário definir dinamicamente um limite de temperatura por meio de um potenciômetro,
possibilitando adaptação em tempo real conforme a necessidade.

As leituras são processadas e exibidas em um display OLED, incluindo:

temperatura atual
umidade relativa do ar
limite configurado
variação entre leituras consecutivas

Além disso, o sistema mantém um histórico limitado das medições em buffers internos, permitindo o cálculo de diferenças
entre valores recentes sem crescimento indefinido de memória. Um LED é utilizado como atuador, sendo acionado sempre que
a temperatura ultrapassa o limite definido.

---

## 2️⃣ Arquitetura do Sistema Embarcado

O sistema segue um modelo de execução sequencial baseado em iterações, simulando o comportamento de um loop embarcado.

A cada ciclo de execução, as seguintes etapas são realizadas:

**Aquisição de dados**
- Leitura de temperatura e umidade via sensor DHT22
- Leitura do valor analógico do potenciômetro via ADC

**Processamento**
- Conversão do valor do potenciômetro para um limite de temperatura dentro do intervalo do sensor (-40°C a 80°C)
- Cálculo da variação (delta) em relação à última leitura armazenada

**Controle**
- Comparação da temperatura atual com o limite definido
- Acionamento ou desligamento do LED conforme a condição

**Gerenciamento de histórico**
- Armazenamento das leituras em buffers limitados (FIFO)
- Remoção dos valores mais antigos quando o limite máximo é atingido

**Saída**
- Atualização do display OLED com todas as informações relevantes

---

## 3️⃣ Componentes Utilizados na Simulação

- **Sensor DHT22:**
Responsável pela medição de temperatura e umidade do ambiente.

- **Potenciômetro (ADC):**
Utilizado como interface de entrada para definição dinâmica do limite de temperatura.

- **Display OLED SSD1306:**
Responsável pela exibição dos dados do sistema em tempo real.

- **LED:**
Atua como sinalizador visual de alerta quando a temperatura excede o limite configurado.

- **Microcontrolador ESP32 (simulado no Wokwi):**
Executa a lógica principal do sistema e integra todos os componentes. 

---

## 4️⃣ Decisões Técnicas Relevantes

- **Mapeamento do potenciômetro para faixa real do sensor:**
O valor analógico (0–4095) foi convertido para o intervalo de temperatura suportado pelo DHT22 (-40°C a 80°C),
garantindo coerência entre entrada do usuário e medições.

- **Uso de buffers limitados (FIFO):**
As leituras são armazenadas em listas com tamanho máximo definido, evitando crescimento indefinido de memória.

- **Cálculo de variação entre leituras:**
A diferença entre valores consecutivos foi incluída para fornecer uma visão mais dinâmica do comportamento das medições.

- **Uso de temporização simples (delay):**
Foi adotado um modelo de temporização baseado em atraso fixo para simplificar a implementação no ambiente de simulação.

---

## 5️⃣ Resultados Obtidos

O sistema foi capaz de:

- Realizar leituras consistentes de temperatura e umidade
- Permitir ajuste dinâmico do limite de temperatura via potenciômetro
- Acionar corretamente o LED quando o limite é ultrapassado
- Exibir todas as informações relevantes no display OLED em tempo real
- Calcular e apresentar a variação entre leituras consecutivas

Durante a simulação no Wokwi, o comportamento do sistema se manteve estável e condizente com os requisitos propostos.

---

## 6️⃣ Comentários Adicionais

Devido às limitações de tempo da execução no ambiente de CI, o loop principal foi implementado com um número finito de
iterações. O intervalo de atualização também foi reduzido para garantir a execução completa dentro do tempo disponível.

Atualmente, os dados históricos são mantidos apenas em memória volátil, sendo descartados conforme o buffer atinge seu
limite máximo. Como melhorias futuras, poderiam ser implementados:

- Persistência de dados (armazenamento externo ou arquivo)
- Tratamento de falhas de leitura do sensor
- Substituição do delay por temporização não bloqueante
- Estrutura de dados mais robusta para armazenamento das medições