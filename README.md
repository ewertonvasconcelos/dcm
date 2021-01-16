# DCM - Data Center Manager 
## Universidade Federal do Rio de Janeiro
## Projeto de Graduação para o Curso de Engenharia Eletrônica e Computação
> Aluno
Ewerton Vasconcelos da Silva

> Orientador
Rodrigo de Sousa 

> Objetivos
Sistema com componentes de software e hardware capaz de fazer a gestão de um conjunto de servidores fornecendo um conjunto de funcionalidades tais como: 
* Ligar/Desligar/Reiniciar ;
* Acesso à BIOS;
* Montar mídia externa (reinstalação de sistema operacional);
  
-----
# Instalando

* Sistema Operacional: Esse projeto foi desenvolvido e testado em uma distribuição Ubuntu 18.04

```
$ git clone https://github.com/ewertonvasconcelos/dcm.git
$ cd dcm
$ ./install_env.sh
```

# Problemas enfrentados
## Teclado:
- Teste com PS2 com arduino que eu tinha: placas legado, não funcionava em todos os SOs e tem problemas com a bios (teclas enter);
- Novo arduíno: Arduino leonardo com conexão HID, funciona como mouse e teclado USB, biblioteca padrão tem problemas no "keyboard boot protocol", não funciona tecla enter
porém funciona as demais teclas direcionais e F10, etc...
- Captura na interface web teve ser ser alocada dentro de uma tag "a" para que fosse feita a captura do teclado com o click na imagem do stream de video.
- Iniciando os testes do Teensyduino que em teoria deve ter compatibilidade com o "keyboard boot protocol", possibilitando o uso do enter na tela de boot.
- a solução se deu com o uso de uma nova biblioteca para o arduino pro micro melhor implementada para omunicação usb, com suporte à simulação de teclado na tela de boot, o Project-HID. (https://github.com/NicoHood/HID")


## Problema Captura de vídeo:
- Testes iniciados com RaspberryPi e captura via Auvidia B101, problemas de estabilidade, preço, limitações do rapberry -> projeto migrou para pc com captura via nova para USB;
- Software testado com melhor desempenho e compatibilidade foi o uStreamer;
- Um problema identificado foi parar o streamer de video quando o usuáro não estava conectado ao sistema. foi feita uma thread que monitora se as portas
reservadas para streaming de video estão com conexão estabelexida, o script é executado a cada 10s, caso não haja nenum cliente esse thread envia uma interrupção para a respectiva instância de video e interrompe o streaming

