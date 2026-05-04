# Processo Seletivo – Intensivo Maker | IoT  
## Etapa Prática – Sistemas Embarcados  

---

### 👤 Identificação  

- **Nome completo:** Gabriel Souza Santos  
- **GitHub:** https://github.com/gabriel-soantos  
- **Projeto no WOKWI:** https://wokwi.com/projects/462374093468124161

---

## 1️⃣ Visão Geral da Solução  

O projeto consiste em um sistema embarcado simulado para monitoramento ambiental utilizando ESP32.
O sistema realiza leitura de temperatura e umidade através do sensor DHT22, permitindo configuração dinâmica de um
limite de temperatura via potenciômetro (ADC).

As informações são processadas em tempo real e exibidas em um display OLED SSD1306, incluindo:

- Temperatura atual  
- Umidade relativa do ar  
- Limite de temperatura configurado  
- Variação entre leituras consecutivas  
- Tendência de comportamento das variáveis (+, -, =, ~)  

Além disso, o sistema mantém um histórico eficiente de medições utilizando um **buffer circular (O(1))**, permitindo
análise de variação sem crescimento de memória.

Um LED é utilizado como atuador, sendo acionado quando a temperatura ultrapassa o limite configurado.

---

## 2️⃣ Arquitetura do Sistema Embarcado  

O sistema segue um modelo de execução sequencial baseado em loop com temporização não bloqueante.

A cada ciclo, o fluxo é dividido em etapas bem definidas:

### 🔹 Aquisição de Dados
- Leitura de temperatura e umidade via DHT22  
- Leitura do potenciômetro via ADC  

### 🔹 Processamento
- Mapeamento do ADC para faixa de temperatura (-40°C a 80°C)  
- Cálculo da variação entre leituras consecutivas  
- Análise de tendência (increasing, decreasing, stable, oscillation)  

### 🔹 Controle
- Comparação da temperatura atual com o limite definido  
- Ativação/desativação do LED conforme condição  

### 🔹 Histórico
- Armazenamento em buffer circular (estrutura O(1))  
- Manutenção de tamanho fixo em memória  

### 🔹 Apresentação
- Atualização do display OLED em tempo real  
- Exibição de valores, deltas e tendências  

---

## 3️⃣ Componentes Utilizados na Simulação  

- **Sensor DHT22:**  
  Responsável pela medição de temperatura e umidade do ambiente.

- **Potenciômetro (ADC):**  
  Interface analógica para ajuste dinâmico do limite de temperatura.

- **Display OLED SSD1306:**  
  Exibição dos dados em tempo real.

- **LED:**  
  Atuador visual de alerta térmico.

- **ESP32 (simulado no Wokwi):**  
  Plataforma de execução do sistema embarcado.

---

## 4️⃣ Melhorias Arquiteturais Implementadas  

### 🔹 Modularização do sistema  
O projeto foi refatorado em módulos independentes:

- `analysis.py` → cálculo de tendências  
- `display.py` → abstração da interface OLED  
- `circular_buffer.py` → estrutura de dados O(1)  
- `main.py` → orquestração do sistema  

---

### 🔹 Buffer circular (O(1))  
Substituição de listas dinâmicas por estrutura circular fixa, garantindo:

- Inserção O(1)  
- Uso controlado de memória  
- Sem realocação de lista  

---

### 🔹 Análise de tendência  
Foi adicionada lógica para identificar comportamento das variáveis:

- `+` → crescente  
- `-` → decrescente  
- `=` → estável  
- `~` → oscilação  

---

### 🔹 Separação de responsabilidades  
O sistema foi reorganizado seguindo princípios de engenharia de software:

- Sensor layer  
- Processing layer  
- Control layer  
- Presentation layer  

---

## 5️⃣ Resultados Obtidos  

O sistema foi capaz de:

- Realizar leituras consistentes de sensores  
- Permitir ajuste dinâmico de limite via potenciômetro  
- Detectar tendências de variação das variáveis  
- Acionar corretamente o LED de alerta  
- Exibir dados completos em tempo real no OLED  
- Manter histórico eficiente com uso de buffer circular  

Durante a simulação no Wokwi, o comportamento se manteve estável e coerente com os requisitos definidos.

---

## 6️⃣ Comentários Adicionais

Devido às limitações de tempo da execução no ambiente de CI, o loop principal foi implementado com um número finito de
iterações. O intervalo de atualização também foi reduzido para garantir a execução completa dentro do tempo disponível.

Atualmente, os dados históricos são mantidos apenas em memória volátil, sendo descartados conforme o buffer atinge seu
limite máximo. Como melhorias futuras, poderiam ser implementados:

- Persistência de dados
- Tratamento de falhas de leitura do sensor
- Comunicação via MQTT ou Wi-Fi (IoT real)  
- Substituição do loop por máquina de estados  
- Logging estruturado de métricas