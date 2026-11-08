# Pokémon HeartGold Definitive Edition — checkpoint 0

Data: 07/11/2026. Estado: preparação parcial; nenhuma ROM ou funcionalidade validada.

## Decisão técnica

Jogo escolhido: HeartGold US, inglês, sem patches nem tradução.
SHA-1 esperado: `4fcded0e2713dc03929845de631d0932ea2b5a37`.
O hash identifica a edição; não comprova a origem legítima.

Candidato principal: https://github.com/ctrl-cheeb-del/pokeheartgold
Commit inspecionado: `cb614ad23449d5852b40321dc409c4143872b35c`.
A adoção definitiva depende de compilação reproduzível e execução em emulador.
Referência e alternativa: https://github.com/pret/pokeheartgold
Commit inspecionado: `e1d5a4606640e31c44d36714ad0b5cdd9c8763fd`.
Ambos foram clonados localmente. Nenhuma alteração de funcionalidade foi aplicada.

O pret declara que está incompleto e alerta para alterações de tamanho/layout.
O fork declara reconstrução integral, mas isso NÃO foi comprovado nesta sessão.
Seu docs/progress/progress.json refere-se a outro commit
(29190e5fb7238c424ea97075e711f58cde55c5d8), com tracked_worktree_dirty=true.
A métrica source_files_in_c=100% não significa ausência de assembly:
o relatório também discrimina assembly original, inline, veneers e código gerado.
Portanto esse relatório não substitui compilar o commit escolhido e comparar bytes.

Outras opções pesquisadas:
- https://github.com/jjrosswurm/pokeheartgold_decomp — fork que também declara reconstrução completa; não compilado aqui.
- https://github.com/EnriqueGF/pokeheartgold-slop — declara cobertura parcial; não compilado aqui.
- https://github.com/BluRosie/hg-engine — alternativa de engine com mudanças amplas de batalha, espécies e mecânicas; não escolhida por destoar da preservação do jogo original.

## Ambiente e tentativas reais

Ambiente Linux x86_64, usuário sem privilégios administrativos.
Disponíveis: Git, GNU Make, GCC/G++, Python 3, pkg-config, wget, xz.
Não encontrados no PATH: ARM GCC, Wine/winepath, Ninja, NASM, Bison, Flex,
melonDS, DeSmuME, xdelta3. libpng não foi encontrado via pkg-config.

1. `make -j2` no fork: falhou ao compilar nitrogfx por ausência de png.h;
   também informou winepath ausente. Saída final: código 2.
2. `make -j2` no pret: baixou Meson 1.12.0 e metroskrew 0.1.3;
   falhou na configuração porque mwccarm não pôde executar. O executável é
   ELF i386 de 32 bits e exige /lib/ld-linux.so.2. Saída final: código 2.
3. Instalação via apt-get falhou por ausência de acesso administrativo ao dpkg.
4. Tentativa de download de pacotes sem instalação falhou porque os pacotes
   não estavam disponíveis nos índices locais. Instalações locais alternativas
   ainda precisam ser investigadas; não se concluiu inviabilidade do ambiente.

Requisitos documentados do fork: Make, Git, compiladores C/C++ do host,
ARM binutils, Wine, Python, libpng, pkg-config e pugixml;
Metrowerks 2.0/sp2p2 e ferramentas/templates compatíveis do Nitro SDK.
O Makefile também seleciona Metrowerks 1.2/sp2p3 para certos objetos.
INSTALL.md exige que arquivos proprietários de compilador e SDK sejam
fornecidos legitimamente. Eles não foram fornecidos nem obtidos nesta sessão.
O pret usa uma cadeia mais recente baseada em Meson/metroskrew e subprojetos;
esta é uma alternativa a avaliar antes de pedir ao usuário ferramentas adicionais.

Nenhuma compilação chegou a produzir ROM. Não houve teste em emulador,
comparação de ROM, teste de save ou validação de campanha.
Debug e Release ainda não foram configurados.

## Primeira melhoria: TMs infinitas

Local identificado nas duas bases: src/party_menu_items.c,
função PartyMenu_LearnMoveToSlot, aproximadamente linhas 896–910 no fork.
Após gravar o movimento e seus PP, a rotina chama Bag_TakeItem quando
MoveIsHM retorna falso. Foram identificadas chamadas a essa rotina nos
caminhos de aprendizado do menu. Isso é análise estática, não validação completa.

Alteração prevista: impedir o consumo de TMs nesse caminho, preservando
compatibilidade, PP e efeitos de amizade/humor. Não alterar a função global
de retirada de itens, pois ela também atende consumíveis comuns.
Arquivos de jogo alterados: nenhum. Patch: ainda não produzido.

Validação exigida depois da compilação original:
- ensinar TM com espaço vazio e com substituição de movimento;
- repetir o uso, inclusive com uma única unidade na mochila;
- recusar Pokémon incompatível, movimento já conhecido e cancelamento;
- verificar HMs e consumo normal de poções/itens evolutivos;
- salvar, fechar, abrir e conferir inventário/movimentos;
- produzir patch e verificar que sua aplicação reproduz o hash da build modificada.

## NPC de evolução por troca

Não iniciado, condicionado à validação das TMs.
Ponto identificado: src/pokemon.c, GetMonEvolution, casos EVO_TRADE e
EVO_TRADE_ITEM. Será necessário integrar a rotina normal de evolução e
verificar itens, cancelamento e preservação de dados. Nenhum NPC foi inserido.

## Escopo e portas de aprovação

V1.0: TMs infinitas; HMs sem ensino mantendo progressão; NPC de evolução
em todos os Centros; chocagem instantânea; exclusivos de versão; eventos
pós-Red; escolhas restantes; Eevee por localidade; espécies faltantes em
Alph; Hard Mode opcional; campo magnético. Nuzlocke excluído.
A lista definitiva de espécies/critério de Alph e as equipes de Hard Mode
serão submetidas à aprovação antes da implementação.

Ordem: compilação original e emulação → TMs e testes → NPC e testes →
demais etapas do pedido. Não acumular funcionalidades não validadas.

## Próximo insumo necessário

Anexar ROM original legítima de HeartGold US em .nds, ou compactada em .zip,
sem tradução, randomizador, patch antipirataria ou outra modificação.
O usuário não precisa calcular o hash: verificar_rom.py faz isso.

Uso pela equipe de desenvolvimento:
`python3 verificar_rom.py caminho/rom.nds --backup-dir caminho/original`
O script recusa hash divergente, não altera a entrada e não sobrescreve
backup existente. A cópia aprovada é verificada e marcada somente leitura.
Testado aqui apenas o caminho de rejeição com dados sintéticos e a ajuda.
O caminho de aceitação/cópia aguarda a ROM real.

Este pacote contém apenas documentação e ferramenta própria de verificação.
Não contém ROM, assets do jogo, SDK nem compilador proprietário.
