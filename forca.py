#!/usr/bin/python3.8 -B 

"""
   Vamos refazer o jogo da forca, porém agora
utilizando a bilioteca curses, para melhor animação
do jogo.
"""
# minha biblioteca:
from lib import motor, perfil, tabuleiro
#import lib.perfil
# bibliotecas do Python:
import sys, pickle, os
from curses import *
from time import time

# dados importantes:
LINHAS, COLUNAS = tabuleiro.LINHAS, tabuleiro.COLUNAS

# mostra as partidas realizadas anteriormentes, ou
# uma parte dela.
def mostra_partidas_aglomerado():
	try:
		# tenta abrir arquivo.
		arq = open(perfil.arq_aglomerado,'rb')
		partidas=[]
		try:
			while True:  partidas.append(pickle.load(arq))
		except EOFError: ... 
		except io.UnsupportedOperation:
			print('o arquivo está vázio.')
			sys.exit()
		finally:
			print('\nquantia de partidas realizadas:%3i' % len(partidas))
			# déz últimas partidas feitas em ordem decrescente
			sublista = partidas[-1:-10:-1]; sublista.reverse()
			# se houver mais de dez registros de partidas.
			if t:=len(partidas) > 10:
				# exibindo quantas irão sair na saída do terminal.
				string = 'mostrando partidas:'+', '.join([str(p.ordem)+'º' for p in sublista])
				print(string)
				# mostrar apenas dez, e os dez últimos feitos.
				for p in sublista: print(p)
			else:
				# caso contrário, mostrar tudo.
				for p in partidas: print(p)
		arq.close()
	except FileNotFoundError: print('arquivo não existe.')

# opção para visualizar partida.
if len(sys.argv) == 2 and sys.argv[1] == 'últimas_partidas_feitas':
	# lista na saída do terminal as partidas
	# realizadas conforme programada anteriormente.
	#lib.perfil.mostra_partidas()
	mostra_partidas_aglomerado()
	# saíndo do programa.
	sys.exit('partidas realizadas acima.'.upper())
elif len(sys.argv) == 2 and sys.argv[1] == 'comandos':
   texto = """\n   𐎚 "últimas_partidas_feitas" - mostra todas, ou pelo menos, 
                                 as últimas partidas realizadas 
                                 no jogo recentemente.\n
   𐎚 "comandos" - mostra essa tela de ajuda. \n"""
   print(texto)
   sys.exit('')

# Simula uma breve pausa no programa.
# Tal tempo pausado tem que ser passado
# como argumento.
def breve_tempo(t):
 	to = time()
 	while abs(to-time()) < t: pass

# função "main" que executa o jogo.  
def executa(janela):
	# inicia janela.
	janela = initscr() # cobre toda tela do terminal.
	noecho() # desabilita o echo ao digitar.
	curs_set(False) # ocultando cursor.
	# desenha uma tela na borda do jogo.
	janela.border(0,0,0,0,0,0,0,0)
	# buscando palavra-chave do jogo.
	motor.palavra_chave = motor.palavra_aleatoria()

	# perfilando partida.
	p = perfil.Perfil(motor.acertos, motor.erros, motor.palavra_chave, motor.dica)
	p.marca_tempo() # começa a conômetrar...

	# roda o bloco enquanto o jogo não estiver finalizado.
	while not motor.partida_finalizada():
		# formando o tabuleiro.
		tabuleiro.desenha_forca(janela)
		tabuleiro.atualiza_tela(motor.acertos, motor.erros, 
			                motor.palavra_chave, motor.dica, janela)
		# entrada da "peça" jogada.
		p.marca_jogada() # começa a registrar a jogada.
		# colocando a opção de abandonar o jogo.
		try:
			# entrada peça.
			jogada = chr(janela.getch())
		except KeyboardInterrupt:
			p.marca_tempo()
			tabuleiro.quadro_resultado(5,29, 'jogo abandonado'.upper(),
									'tempo decorrido:%2.2f' %p.tempo,
									'palavra correta: "%s".'% p.palavra_chave,
									'erros: %i cometidos'%len(p.erros),
									'dica do jogo: "%s"'%p.dica)
			beep() # emite um sinal ao acionar isto.
			janela.refresh() # atualiza para escrita na tela.
			breve_tempo(3)
			del p # apaga dado desnecesário.
			sys.exit('saindo do jogo... feito.')
		# faz uma jogada, e, registra se foi aceita.
		# Falso se não, pois é inválida a entrada ou,
		# a tecla já foi digitada. E, o caso contrário
		# é o valor lógico verdadeiro.
		resultado = motor.joga(jogada)
		# registra tempo da jogada.
		p.marca_jogada(peca=jogada)
		# Se for "True" então foi uma jogada acertada.
		# Caso contrário, então foi um, erro, ou seja 
		# vamos marca-lo. Porém..., se a peça já foi 
		# registrada com errada, não marcar.
		if not resultado: tabuleiro.marca_forca(janela)
		# última atualização de tela.
		tabuleiro.atualiza_tela(motor.acertos, motor.erros, 
						motor.palavra_chave, motor.dica, janela)
		# termina a conometragem da partida.
		p.marca_tempo()
		# marca o resultado.
		p.marca_resultado(motor.e_vitorioso())
		# marca a tela do jogo.
		p.captura_tela = tabuleiro.captura_tela(janela)
		# atualizando acertos e erros.
		p.acertos = motor.acertos
		p.erros = motor.erros

	# armazenada info da partida.
	perfil.armazena(p)
	# mostrando o resultado do jogo.
	mensagem = ('você venceu o jogo!', 'você perdeu o jogo!')
	# apagando tudo do tabuleiro, menos a 
	# estrutura da forca. A contagem de erros é
	# para mostrar até onde o boneco foi.
	tabuleiro.limpa_tabuleiro(len(motor.erros), janela)
	if motor.e_vitorioso(): 
		# colocando reultado com informações importantes.
		tabuleiro.quadro_resultado(5,29,mensagem[0].upper(),
									'tempo decorrido: %0.2f seg' % p.tempo,
								 	'palavra correta: "%s".'% p.palavra_chave,
									'erros: %i cometidos'%len(p.erros),
									'dica do jogo: "%s"'%p.dica)
		#'tempo decorrido: %0.2f seg' % p.tempo,
	else: 
		# Exibindo mensagem do resultado da partida.
		# Info básica sobre o jogo.
		tabuleiro.quadro_resultado(5,29,mensagem[1].upper(),
						'tempo decorrido: %0.2f seg' % p.tempo,
						'palavra correta: "%s".'% p.palavra_chave,
						'acertos: %i realizados'%len(p.acertos),
						'dica do jogo: "%s"'%p.dica)
		# 'tempo decorrido: %0.2f seg' % p.tempo,
	# faz o backup do registro, independente da plataforma.
	perfil.faz_backup()
	# breve pausa para visualizar resultado.
	breve_tempo(3)
	janela.refresh() # último impressão da tela.
	endwin() # encerra tela de jogo.

# execução do programa.
if __name__ == '__main__':
	# execuntado pelo "wrapper" que defaz 
	# bagunça na tela após erros, e, ainda 
	# ativa automáticamente a coloração.
	wrapper(executa)
	# visualização prévia da captura de tela futura.
	#print(_str)
