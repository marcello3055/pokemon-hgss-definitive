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
