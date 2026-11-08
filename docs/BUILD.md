# Reconstrução — instruções para o agente

O usuário não precisa executar estes comandos. São instruções de retomada técnica.

## Base fixa e dados separados
Consultar upstream.lock.json. Baseline e tm-wip são diretórios distintos em .work/.
Não confundir esses nomes com as futuras configurações Debug e Release.
A fonte original é obtida do upstream, nunca incorporada ao histórico deste projeto.
A ROM do usuário fica fora do repositório ou em originals/ (ignorado).

## Linux Debian x86_64 sem privilégios administrativos
Pré-requisitos do host: Bash, Python 3, Git, make, gcc/g++, pkg-config, dpkg-deb,
apt-get, wget, xz e chaveiro Debian. A rede deve permitir Debian, GitHub e PyPI.

1. Verificar ROM e preservar original, usando pasta de backup ainda inexistente:
   python3 scripts/verify_rom.py /caminho/rom.nds --backup-dir originals
2. Instalar dependências locais:
   bash scripts/setup_rootless.sh
3. Reproduzir original:
   bash scripts/build.sh baseline
4. Conferir igualdade de bytes, além do SHA-1:
   cmp originals/heartgold-us-original.nds artifacts/baseline/heartgold.nds
5. Compilar alteração WIP:
   bash scripts/build.sh tm-wip

O modo baseline executa make com os testes originais. O modo tm-wip usa make rom:
é esperado que os checksums originais não correspondam a uma ROM modificada.
Nunca usar essa ausência de comparação como prova de correção.

A instalação local reconstrói a solução executada anteriormente: pacotes Debian
extraídos sem root; patchelf para loader/rpath i386; wrappers QEMU para todos os ELF
de 32 bits do metroskrew, inclusive arquivos .exe. M4 e variáveis de pkg-config
para a máquina de build são necessários. Os pacotes Debian podem receber atualizações;
o script registra SHA-256 dos downloads em .work/deps/packages.sha256. Isso não é um
lock completo do ambiente. Após uma reconstrução validada, preservar esse manifesto.

Os scripts consolidados foram reconstituídos após perda do ambiente. Validação de
sintaxe/patch não equivale a terem executado de ponta a ponta nesta nova sessão.

## Emulador programático
python3 -m pip install --target .work/python py-desmume==0.0.9
PYTHONPATH=.work/python python3 scripts/boot_smoke.py artifacts/baseline/heartgold.nds artifacts/baseline/title.png

Examinar a imagem. 1800 frames sem exceção não comprovam jogabilidade completa.
Não carregar estados antigos em builds com layout diferente sem validação.
A falta de display foi resolvida com SDL_VIDEODRIVER=dummy e SDL_AUDIODRIVER=dummy.

## Patch de distribuição (somente após testes)
source .work/deps/env.sh
xdelta3 -e -s originals/heartgold-us-original.nds artifacts/tm-wip/heartgold.nds artifacts/tm-wip/change.xdelta
xdelta3 -d -s originals/heartgold-us-original.nds artifacts/tm-wip/change.xdelta artifacts/tm-wip/reapplied.nds
cmp artifacts/tm-wip/heartgold.nds artifacts/tm-wip/reapplied.nds

Esses comandos documentam o procedimento; não indicam que o patch foi produzido.
Publicar somente patch e instruções, nunca a ROM.

## Checkpoint
Atualizar PROGRESS.md e docs/TESTS.md. Revisar diff; adicionar só arquivos permitidos.
python3 scripts/audit_repo.py
git commit -m "WIP: descrição verdadeira do marco"
python3 scripts/checkpoint.py /caminho/fora-do-repo/checkpoint.zip

O script exige árvore limpa, audita histórico, verifica bundle e faz clone de teste.
O ZIP deve então ser salvo em armazenamento persistente ou enviado ao remoto autorizado.
Sem essa última operação, um commit local pode desaparecer num reinício.

## Correção Ninja e testes ARM (08/11/2026)
Meson espera NINJA como caminho executável, sem argumentos embutidos.
O wrapper criado por build.sh limita a quatro tarefas. Duas builds passaram com
esta correção antes do reinício; código reconstituído do histórico da execução.

python3 -m pip install --target .work/python unicorn==2.1.4 pyelftools==0.32
PYTHONPATH=.work/python python3 scripts/test_tm_arm.py .work/baseline/build/heartgold.us/main.nef .work/tm-wip/build/heartgold.us/main.nef artifacts/tm-wip/arm-tests.json
PYTHONPATH=.work/python python3 scripts/compare_tm_builds.py .work/baseline/build/heartgold.us/main.nef .work/tm-wip/build/heartgold.us/main.nef artifacts/baseline/heartgold.nds artifacts/tm-wip/heartgold.nds artifacts/tm-wip/binary-comparison.json

NEF contém símbolos; main.sbin contém o código residente a executar. O comparador
só cobre código residente e endereços/tamanhos de funções; não valida gameplay.
Não versionar logs brutos de Meson: podem conter variáveis de ambiente. Registrar
somente resultados sanitizados. Testes ARM simulam serviços externos e não
substituem validação pela interface e salvamento.
