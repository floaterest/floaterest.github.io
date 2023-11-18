# for each file in commandline argument do
for f in "$@"; do
    fontforge nerd-fonts/font-patcher "$f" -c -q --no-progressbars -out nerd
done