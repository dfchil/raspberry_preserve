set terminal svg size 1280,720 solid linewidth 0.7
set output 'hotmoist.svg'

# load "override.terminal.gp"



set lmargin 4.5
set bmargin 6.0
set rmargin 3.0
set tmargin 0.4

set key right top

unset xlabel
unset ylabel

set datafile separator ","

set timefmt '%Y-%m-%d %H:%M'
set yrange [ 0 : 80]
set xdata time


plot \
'hotmoist.data' \
    using 1:2 with lines linecolor rgb "blue" title 'Luftfugtighed', \
'' \
    using 1:3 with lines linecolor rgb "red" title 'Temperatur', \
