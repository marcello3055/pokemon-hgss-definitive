# Progresso — 08/11/2026

## Estado atual
Base: HeartGold US em inglês; pret/pokeheartgold fixado em upstream.lock.json.
Repositório privado: https://github.com/marcello3055/pokemon-hgss-definitive
Acesso de leitura e escrita confirmado. Primeiro envio remoto: d5bd81fdd8583ccf03080dc856db3e8a170bb65e.

TMs infinitas: compilação e testes de rotinas ARM passaram na execução anterior;
ainda WIP, sem validação completa pela interface. Nenhuma melhoria V1.0 está
marcada como concluída. NPC de evolução ainda não iniciado.

## Resultados observados antes do novo reinício do ambiente
- Original fornecido: 134217728 bytes, SHA-1 4fcded0e2713dc03929845de631d0932ea2b5a37.
- Baseline recompilada: make terminou com código 0; quatro testes originais passaram,
  zero falhas; SHA-1 correto e cmp com original terminou sem divergência.
- ROM baseline recompilada abriu no DeSmuME; tela de título inspecionada.
- Build tm-wip terminou com código 0.
- Testes ARM com Unicorn passaram nas duas builds: 12 casos por build (quantidades
  1, 2, 99 x quatro espaços de movimento), 20 repetições na modificada, HM preservada
  e aprendizagem sem item. Código real de aprendizagem e Bag_TakeItem; serviços de
  Pokémon, PP, metadados e amizade simulados. Isso NÃO testa interface ou saves.
- Original jogado até New Bark Town; personagem de teste A. Estado não persistido.
- Comparação binária iniciada, resultado NÃO observado. Não declarar layout validado.
- Abertura da ROM modificada ainda não executada/observada.

Ao receber a solicitação de economia de créditos, os processos anteriores já não
existiam e os arquivos locais haviam retornado ao checkpoint cdf65c8. Binários,
logs integrais, resultados JSON e estados de emulador não sobreviveram. O remoto
foi conferido e os scripts recuperados do registro desta conversa. Os resultados
acima são evidências históricas observadas, não arquivos de teste reapresentados.
O comparador foi simplificado na recuperação; não foi executado nesta versão.

## Correções e arquivos próprios
- scripts/build.sh: NINJA agora aponta para wrapper executável com -j4. A forma
  anterior NINJA="ninja -j4" causava erro de detecção do Meson. Correção usada com
  sucesso nas duas compilações anteriores.
- scripts/test_tm_arm.py: teste de rotinas compiladas, reconstruído após reinício.
  NEF fornece símbolos; código residente vem de main.sbin, pois seções NEF têm tamanho zero.
- scripts/compare_tm_builds.py: comparação de endereços/tamanhos e bytes residentes.
- patches/0001-infinite-tms-WIP.patch: quantidade retirada da TM de 1 para 0 em
  PartyMenu_LearnMoveToSlot, src/party_menu_items.c. Sem outras alterações no jogo.

## Próximo bloco (curto)
1. Conferir GitHub e arquivos existentes antes de reconstruir qualquer coisa.
2. Se binários ausentes, recuperar a ROM já fornecida e executar docs/BUILD.md.
   Não repetir pesquisa de bases ou pedir novo upload enquanto o arquivo existir.
3. Executar comparador e abertura da ROM modificada; persistir resultados textuais
   sanitizados no GitHub IMEDIATAMENTE, antes de iniciar testes pela interface.
4. Testar TM em espaço vazio/substituição, repetições, incompatibilidade,
   cancelamento, HMs, consumíveis e salvar/reabrir. Ferramentas Debug só conforme necessário.
5. Gerar patch binário e verificar reaplicação. Somente então avançar ao NPC.

## Política de créditos e checkpoints
Usuário pediu economia e reserva de créditos. Não temos acesso ao saldo nem medição
confiável de custo por operação; NÃO prometer parada automática por saldo.
Trabalhar em blocos menores; enviar scripts antes de operações demoradas e evidências
sanitizadas logo após cada marco. Evitar grandes blocos sem checkpoint remoto.
Nesta retomada, preservar código/resultados e encerrar o bloco sem recompilação longa.

## Demais funcionalidades
NPC de troca, chocagem instantânea, Eevee por localidade, campo magnético,
exclusivos de versão, HMs sem ensino, eventos pós-Red, escolhas exclusivas,
Alph e Hard Mode ainda não implementados. Debug/Release ainda não separados.
Lista/requisitos de Alph e equipes Hard Mode dependem de aprovação futura.
Nuzlocke fora do escopo. Não publicar ROM, assets, SDK, BIOS, ferramentas ou saves.
