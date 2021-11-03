# descrição dos elementos do jogo-da-forca
Um jogo da forca simples feito em Python, com a biblioteca "semigráfica": `ncurses`. O jogo é bem intuitívo quando inicializado, têm: dois campos(um para letras de acerto, outro para erros); a forca e o bonequinho que vai aparecendo; também o campo da pontuação, que basicamente conta as letras acertas e erradas; e o campo de dica com o tema da palavra perguntada. Ao ganhar ou perder, aparece um campo com algumas informações básicas da partida jogada, sabe, o tempo de duração as teclas apertadas na sequência,... se venceu ou não a partida, a verdadeira palavra que estava se buscando e etc.

# registros das partidas
Todas as partidas realizadas são registradas, com todos dados de final de partida mencionados acima. Um disparo da tela para ver como ficou o "tabuleiro" final, independente do resultado, é também gravado no "banco de dados". Para acessar-lô, visualizar todas suas jogadas, então digite o setup(no caso `forca.py`) do programa a  executar, e o argumento `últimas_partidas_feitas`, ficaria assim no bash: 
  - ./forca.py últimas_partidas_feitas
