set terminal svg size 1280,720 solid linewidth 0.7
set output 'hotmoist.svg'


set lmargin 7.5
set bmargin 6.0
set rmargin 7.0
set tmargin 1.4

set key right top

unset xlabel
unset ylabel

set datafile separator ","



set timefmt '%Y-%m-%d %H:%M'
set xdata time

set ytics 1 nomirror
set ylabel 'Luftfugtighed'

set y2tics 1 nomirror
set y2label 'Temperatur' 

plot 'hotmoist.data' \
    using 1:2 with lines linecolor rgb "blue" title 'Luftfugtighed', \
''  using 1:3 with lines linecolor rgb "red" title 'Temperatur' axes x1y2
