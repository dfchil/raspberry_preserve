set terminal svg size 1280,720 solid linewidth 0.7
set output 'hotmoist.svg'


set lmargin 7.5
set bmargin 6.0
set rmargin 7.0
set tmargin 1.4

set key right top

set yrange [30:75.5]
set y2range [*:27]

set datafile separator ","

set timefmt '%Y-%m-%d %H:%M'
set xdata time

set ytics 5 nomirror tc rgb "blue"
set ylabel 'Humidity' tc rgb "blue"

set y2tics 1 nomirror tc rgb "red"
set y2label 'Temperature'  tc rgb "red"




plot 'data/2014-09.data' \
    using 1:2 with lines linecolor rgb "blue" title 'Humidity', \
''  using 1:3 with lines linecolor rgb "red" title 'Temperature' axes x1y2 , \
	35  with lines lt 0 linecolor rgb "blue" title "Humidity limits", \
	65  with lines lt 0 linecolor rgb "blue" title "", \
	26  with lines lt 0 linecolor rgb "red" title "Temperature max" axes x1y2
	
