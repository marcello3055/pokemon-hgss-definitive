# Progresso — 07/11/2026

## Estado atual
Checkpoint de continuidade criado após reinício do ambiente temporário.
**Último marco funcional observado:** reconstrução do jogo original igual à ROM enviada.
**Funcionalidade em andamento:** TMs infinitas. Alteração recuperada; compilação modificada
foi iniciada antes da interrupção, mas o resultado NÃO foi observado.
Nenhuma melhoria está marcada como concluída.

## Base
- HeartGold US, inglês, ROM SHA-1 4fcded0e2713dc03929845de631d0932ea2b5a37.
- Base de trabalho: pret/pokeheartgold, revisão e1d5a4606640e31c44d36714ad0b5cdd9c8763fd.
- Fork ctrl-cheeb-del continua alternativa, não teve compilação validada.
- Não alterar a revisão automaticamente. A base pret é parcialmente descompilada.

## Evidências já observadas na execução anterior
1. ROM enviada: 134217728 bytes e SHA-1 correto. Cópia local somente leitura criada.
2. Dependências instaladas sem root via pacotes Debian extraídos localmente.
3. Ferramentas i386 executadas com QEMU e loader local.
4. Compilação original terminou; quatro testes de checksum passaram (ARM9, ARM7,
   filesystem e ROM). Hash da ROM reconstruída igual ao original.
5. ROM original executou em DeSmuME via py-desmume; imagens de abertura e título
   inspecionadas. Introdução avançada até as telas finais do Professor Oak.
6. Teste explícito de abertura da ROM recompilada iniciado; resultado final não inspecionado.
7. Alteração em src/party_menu_items.c: quantidade retirada da TM passa de 1 para 0,
   mantendo a chamada e visando preservar o layout. Compilação modificada iniciada.

Os binários, logs completos, capturas e estados de teste acima foram perdidos no
reinício. Esses itens são evidência histórica da conversa, não arquivos anexos neste
checkpoint. Não inventar novo resultado nem declarar teste de TMs concluído.

## Recuperação desta execução
- Checkpoint 0 restaurado e lido. Seu relatório é histórico e foi superado por este.
- Patch WIP reconstituído a partir da alteração registrada e fonte da revisão fixa.
- Scripts de reconstrução e teste reconstituídos.
- Histórico Git próprio criado; arquivo bundle e restauração de teste fazem parte
  do procedimento de checkpoint.
- Usuário autorizou conectar GitHub e criar pokemon-hgss-definitive PRIVADO em
  07/11/2026. Conexão confirmada na conta marcello3055.
  As ferramentas disponíveis não incluem criação de repositório; gh CLI não autenticado
  e navegador separado está na tela de login. Consulta do destino retornou 404
  (não encontrado ou sem acesso). Aguardar criação manual de repositório PRIVADO
  pokemon-hgss-definitive, com README, e então usar APIs de conteúdo/Git para envio.
  Não pedir autorização novamente.
- Resultados de auditoria e restauração: ver docs/TESTS.md e relatório do checkpoint.

## Próxima ação de desenvolvimento
1. Restaurar repo/bundle e conferir HEAD/status/PROGRESS antes de agir.
2. Recuperar a ROM já fornecida, sem pedir novo envio enquanto ela estiver disponível.
3. Reconstituir ambiente com docs/BUILD.md. A reconstrução é necessária porque os
   binários foram perdidos; não repetir a pesquisa de bases nem rediscutir o escopo.
4. Gerar baseline e tm-wip; conferir hash original, alterações binárias e layout.
5. Testar uso real de TM (vaga livre/substituição), repetições, incompatibilidade,
   cancelamento, HMs, consumíveis e salvar/reabrir.
6. Criar patch binário, aplicar a uma cópia original e comparar resultado.
7. Só após validação das TMs avançar ao NPC de evolução.

## Escopo e status
| Funcionalidade | Estado |
|---|---|
| TMs infinitas | WIP, sem validação final |
| NPC de evolução por troca em todos os Centros | Não implementado |
| Chocagem instantânea | Não implementada |
| Eevee por localidade | Não implementada |
| Campo magnético | Não implementado |
| Exclusivos de versão | Não implementado |
| HMs sem ensino, preservando progressão | Não implementado |
| Eventos pós-Red | Não implementados |
| Escolhas mutuamente exclusivas restantes | Não implementadas |
| Espécies indisponíveis / Alph | Análise e aprovação pendentes |
| Hard Mode | Estrutura/equipes e aprovação pendentes |
| Debug/Release separados | Ainda não configurados |

Nuzlocke não faz parte da V1.0. Não garantir compatibilidade com versão futura.

## Decisões reservadas ao usuário
- Lista final de espécies e requisitos de Alph.
- Equipes e chefes adicionais do Hard Mode.
- GitHub privado já autorizado. Conta conectada; falta criar/acessar o repositório de destino.

## Atualização: repositório criado pelo usuário
O usuário informou a criação de pokemon-hgss-definitive. Consulta de
marcello3055/pokemon-hgss-definitive ainda retornou 404. list_repositories,
list_installations e list_installed_accounts retornaram listas vazias.
Não interpretar isso como prova de que o usuário não criou o repositório: falta
confirmar URL e conceder acesso à instalação/conexão. Nenhum arquivo enviado.
O script setup_rootless.sh concluiu com sucesso nesta execução (pacotes locais),
e prepare_source.py baseline recuperou exatamente o commit fixado. Ainda não
foi repetida a compilação completa. Próximo comando local: bash scripts/build.sh baseline.

## Acesso GitHub resolvido — 07/11/2026
Instalação 179663552 confirmada na conta marcello3055. Repositório privado
marcello3055/pokemon-hgss-definitive acessível com pull/push. README inicial
remoto preservado no histórico. Checkpoint local será publicado via API Git;
o bundle dos commits locais anteriores permanece no checkpoint 4.
Reconstrução baseline iniciada novamente; resultado ainda pendente.
