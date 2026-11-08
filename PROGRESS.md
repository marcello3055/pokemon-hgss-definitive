# Progresso — 08/11/2026

## Estado atual
Base: HeartGold US em inglês; pret/pokeheartgold fixado em upstream.lock.json.
Repositório privado: https://github.com/marcello3055/pokemon-hgss-definitive
Acesso de leitura e escrita confirmado. Primeiro envio remoto: d5bd81fdd8583ccf03080dc856db3e8a170bb65e.

TMs infinitas: compilação e recuperação do patch confirmadas; comparação binária
aprovada em 08/11/2026. Testes ARM novamente executados e aprovados em 08/11/2026. Ainda WIP,
sem validação completa pela interface. Nenhuma melhoria V1.0 está
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

## Bloco pequeno concluído — 08/11/2026
- Remoto abe482a conferido; arquivos locais íntegros e dependências locais presentes.
- Criado scripts/validate_tm.py, com etapas independentes e relatórios atômicos.
- Preflight executado: bloqueio esperado, seis arquivos compilados ausentes;
  resultado em docs/validation-preflight.json. Sintaxe Python e conteúdo do relatório
  verificados. Etapas binary/arm/boot do novo executor ainda não exercitadas.
- Nenhuma recompilação ou nova validação de gameplay neste bloco.
- Próximo bloco: reconstruir somente baseline e salvar resultado sanitizado. Depois,
  reconstruir tm-wip; executar cada etapa de validação e registrar imediatamente.

## Baseline reconstruída e preservada — 08/11/2026
- scripts/build.sh baseline terminou com código 0 nesta execução.
- Quatro testes de checksum OK; ROM 134217728 bytes e SHA-1 esperado.
- Relatório observado: docs/baseline-validation.json. Emulador não executado neste bloco.
- Dados privados de comparação (main.nef e main.sbin) guardados fora do GitHub em
  HeartGold_Baseline_Private_Test_Cache.zip, Library ID
  libfile_a74f8b46c86c8191a48daf5ebd6b5c4f. ZIP e SHA-256 internos verificados.
  Este cache contém dados derivados do jogo: NÃO enviar ao GitHub nem distribuir.
- Se houver reinício, recuperar esse cache e conferir manifest.json. Recolocar os
  dois arquivos em .work/baseline/build/heartgold.us/. A ROM baseline é idêntica à
  original fornecida: recuperar o ZIP original já existente e conferir SHA-1 antes
  de usá-la como artifacts/baseline/heartgold.nds. Isso evita recompilar baseline.
- Próximo bloco: compilar somente tm-wip, registrar o resultado e guardar seu cache
  privado antes de iniciar a comparação binária. Não reexecutar baseline sem motivo.

## Versão TM recuperada e comparação aprovada — 08/11/2026
- Build tm-wip anterior terminou com código 0; relatório recuperado do cache em
  docs/tm-build-validation.json. Patch xdelta de 321673 bytes teve reaplicação exata.
- Cache privado salvo: HeartGold_TM_WIP_Private_Test_Cache.zip, Library ID
  libfile_ce763427d94c8191868765e786b836fd. Contém main.nef, main.sbin, tm-wip.xdelta,
  manifest.json e validation.json. NÃO versionar ou distribuir dados do cache.
- Novo reinício removeu arquivos temporários. Recuperados os dois caches privados,
  conferidos seus SHA-256 e restaurada a base a partir do ZIP original fornecido.
  A ROM modificada foi recuperada por xdelta, sem recompilar nenhuma variante.
- SHA-1 modificado confirmado: 34f3068802d836309eeb6da01460f9e32b26ad4d.
- Executado validate_tm.py binary: aprovado. Relatórios em docs/binary-comparison.json
  e docs/validation-binary.json. Única diferença no main.sbin: endereço 0x020825aa,
  byte 1 -> 0, dentro de PartyMenu_LearnMoveToSlot. 33952 símbolos de função comparados,
  com mesmos endereços e tamanhos (mapa por nome do comparador).
- ARM9 compactado passou de 762644 para 762648 bytes; rodapé NitroSDK de 12 bytes
  permanece idêntico, deslocado com o tamanho. Fora da região ARM9 + rodapé e do
  cabeçalho, ROM idêntica. Cabeçalho só mudou tamanho ARM9 e CRC.
- Comparador ampliado para verificar regiões não relacionadas e rodapé. Durante a
  investigação, comparação de caudas deslocadas produziu contagem inválida; corrigida
  para offsets absolutos. Só os relatórios finais aprovados foram versionados.
- Este bloco NÃO executou ARM novamente nem emulador. Próximo bloco curto: executar
  validate_tm.py arm usando arquivos recuperados e guardar relatório. Em bloco posterior,
  abrir modificada no emulador e testar interface/save antes de declarar TMs concluídas.
- Para retomar após reinício: restaurar NEF/SBIN de cada cache em .work/VARIANTE/build/heartgold.us;
  restaurar original verificado como artifacts/baseline/heartgold.nds; aplicar tm-wip.xdelta
  ao original para artifacts/tm-wip/heartgold.nds; conferir hashes acima. Não recompilar
  por rotina: os caches preservam os dados necessários aos testes atuais.

## Testes ARM registrados — 08/11/2026
- Executado python3 scripts/validate_tm.py arm com saída 0; relatórios preservados
  em docs/arm-tests.json e docs/validation-arm.json. Nenhuma recompilação.
- Dependência Unicorn 2.1.4 instalada em .work/python; pyelftools 0.32 já presente.
- Baseline: 12 casos (quantidades 1/2/99 x quatro espaços) consumiram 1 TM.
- Modificada: mesmos 12 casos mantiveram a quantidade. Mais 20 chamadas repetidas
  mantiveram a única TM. Cenários HM Cut e aprendizagem sem item passaram nas duas.
- Escritas de movimento, reset de PP Ups e PP conferidas nas chamadas interceptadas.
- Limitação: serviços externos de Pokémon, PP, classificação de item/HM e amizade
  simulados. Não prova compatibilidade de espécies, interface, cancelamento ou saves.
- Nenhuma mudança no código do jogo neste bloco. TMs permanecem WIP.
- Próximo bloco curto: instalar py-desmume 0.0.9 se necessário, executar
  python3 scripts/validate_tm.py boot e inspecionar artifacts/tm-wip/title.png.
  Registrar resultado antes de iniciar testes de ensino pelas telas do jogo.

## ROM modificada inicializada no emulador — 08/11/2026
- Executado validate_tm.py boot, saída 0, 1800 frames com py-desmume 0.0.9.
- Inspeção visual confirmou título HeartGold, Ho-Oh e TOUCH TO START; duas telas
  renderizadas. ROM testada SHA-1 34f3068802d836309eeb6da01460f9e32b26ad4d.
- Relatório em docs/validation-boot.json. Captura preservada fora do GitHub:
  HeartGold_TM_Boot_Verified.png, Library ID libfile_80b6f400fc7c819197f0036aed049922.
- Sem recompilação ou alteração da ROM. TMs ainda WIP: inicialização não comprova
  aprendizagem pela interface, compatibilidade, cancelamento ou save/load.
- Próximo bloco, executado pelo agente: preparar partida de teste na ROM modificada
  e chegar ao primeiro Pokémon. Preservar estado/saves privados para não repetir a
  introdução após reinícios. Depois testar TMs pelos menus e salvar/reabrir.
- Usuário não precisa operar ferramentas ou programar; os próximos blocos também
  são responsabilidade do agente, respeitando pedidos de economia de créditos.
