# Testes pela interface — 08/11/2026

ROM WIP SHA-1: `34f3068802d836309eeb6da01460f9e32b26ad4d`.
Emulador: py-desmume 0.0.9 / DeSmuME 0.9.12, interpretador.

## Preparação e resultado observado

- Retomada do estado da introdução; personagem masculino A.
- Introdução, saída de casa e entrada no laboratório executadas pelos controles.
- Chikorita macho, nível 5, recebido do Professor Elm pelo evento original.
- Salvar pelo menu, exportar backup `.sav`, fechar e reabrir ROM, selecionar
  Continue: personagem e Chikorita recuperados no laboratório, zero insígnias.
- Para o teste, inserida uma única TM17 Protect na bolsa em RAM. Nenhum dado de
  Pokémon ou flag narrativa foi editado. Esta é preparação privada de QA, não
  funcionalidade Debug da ROM nem mudança da progressão destinada ao jogador.
- Bolsa exibiu Protect No.17 x1. Use -> Teach Protect -> Yes -> Chikorita ABLE.
- Interface exibiu `CHIKORITA learned Protect!`. Não houve substituição: havia
  espaço livre. Quantidade em RAM permaneceu 1; reabertura da bolsa exibiu x1.
- Após ensino: salvar pelo menu, confirmar substituição do save de QA, exportar
  `.sav`, fechar e reabrir ROM SEM carregar `.dst`, selecionar Continue.
  Bolsa novamente exibiu Protect x1; resumo de Chikorita exibiu Tackle 35/35,
  Growl 40/40 e Protect 10/10. Persistência do movimento e da TM aprovada neste caso.

## Retomar sem repetir a introdução

Restaurar o arquivo privado indicado em PROGRESS.md em `artifacts/ui-test/`.
Reconstituir a ROM WIP conforme BUILD.md e copiá-la como `test.nds` nessa pasta.
Nunca usar arquivos de um jogador para QA. Para estado rápido:

```sh
PYTHONPATH=.work/python python3 -i scripts/ui_session.py
```

O console confere o hash da ROM e carrega `latest.dst` se existir.
`shot()` grava tela e estado; `key(Keys.KEY_A)` e `tap(x,y)` controlam o jogo.
Coordenadas de toque são relativas à tela inferior (256x192).
Para testar persistência real, abrir ROM com o backup `test.sav`, SEM carregar
estado rápido, e selecionar Continue. `.dst` não comprova save/load.
O exportador aceitou `.sav` e retornou True; tentativa `.dsv` retornou False.
O backup raw tem 524288 bytes. Aguardar o término do salvamento antes de exportar.

## Limites

Este resultado cobre uma espécie compatível e um movimento em espaço livre.
Não valida ainda substituição com quatro movimentos, uso em outra espécie,
cancelamento, espécie incompatível, HMs, consumíveis ou a campanha completa.
TMs permanecem WIP até concluir a matriz de testes.
