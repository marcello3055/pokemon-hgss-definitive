# Registro de testes

## Execução anterior — evidência histórica observada
- ROM enviada e ROM reconstruída: SHA-1 4fcded0e2713dc03929845de631d0932ea2b5a37.
- Build pret: quatro testes passaram, zero falhas (ARM9, ARM7, filesystem, ROM).
- py-desmume: 600 frames e abertura Game Freak; 1800 frames e título HeartGold.
- Verificador de ROM: arquivo inválido rejeitado sem modificar entrada/criar backup;
  ROM real aceita e cópia verificada.
- Logs/binários/imagens locais perdidos no reinício. Não estão disponíveis neste pacote.

## Execução de recuperação
Resultados automatizados são registrados em docs/recovery-test-results.json.
A restauração do bundle e sua comparação com HEAD são registradas em
CHECKPOINT.json dentro do ZIP de backup, após o commit.

## TMs — ainda pendente
- Build modificada e comparação de layout/símbolos.
- Ensino com vaga livre e substituição de movimento.
- Uma TM na mochila; uso repetido em Pokémon diferentes.
- Pokémon incompatível, movimento já conhecido, cancelar antes e durante seleção.
- HMs não consumidas e compatibilidade intacta.
- Poções/itens evolutivos continuam consumidos.
- Salvar, fechar e reabrir; conferir inventário e movimentos.
- Patch binário reaplicado reproduz exatamente o artefato testado.

A alteração passa quantidade zero a Bag_TakeItem apenas no aprendizado TM/HM.
O código original de Bag_TakeItem subtrai a quantidade e compacta o bolso.
Isso sustenta a hipótese, mas não substitui teste de integração.
Preservar offsets deve ser demonstrado por comparação, não presumido.

## Evidência histórica adicional — 08/11/2026
Antes do novo reinício: baseline make exit 0; 4 testes OK / 0 falhas; SHA-1 correto;
cmp original/baseline sem diferenças; título baseline inspecionado no DeSmuME.
Build tm-wip exit 0. test_tm_arm.py passou para baseline e modificada: 12 cenários
por build, repetição 20x na modificada, HM e aprendizagem sem item. Dados de
Pokémon/PP/metadados/amizade simulados, bolsa executada em código ARM real.
Comparador iniciado mas resultado não observado. UI de TMs, save/load modificado
e patch binário pendentes. Binários e logs perdidos; scripts reconstituídos e
sintaxe verificada na retomada, sem repetir compilação para economizar créditos.

## Baseline observada nesta execução (08/11/2026)
Ver docs/baseline-validation.json: quatro checksums OK, build exit 0, tamanho e
SHA-1 da ROM iguais ao esperado. Nenhum novo teste de gameplay neste bloco.

## Comparação binária executada — 08/11/2026
validate_tm.py binary retornou 0. Código residente: um byte 1->0 em 0x020825aa.
Mapa de 33952 símbolos de funções preservado. Rodapé estático preservado; regiões
fora de ARM9/rodapé/cabeçalho idênticas. Mudanças de cabeçalho limitadas a tamanho
ARM9 e CRC. Ver binary-comparison.json e validation-binary.json. Gameplay pendente.

## Testes ARM executados nesta retomada — 08/11/2026
validate_tm.py arm retornou 0: 12 cenários na baseline, 12 na modificada, repetição
20x na modificada, HM Cut e aprendizagem sem item nas duas versões. Ver arm-tests.json
(serviços externos simulados) e validation-arm.json. Interface, compatibilidade de
espécies, cancelamento e salvar/carregar continuam pendentes. Sem recompilação.
