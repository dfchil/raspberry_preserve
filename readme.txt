Goals:
	sample temperature and moisture at given interval
	store data for statistical purposes
	generate alarms if over certain threshhold (send e-mail)
	
	generate plots from stored data
	
implementation:
	data gathering through cron triggered python script 
	above script also triggers alarms
	
	store in flat CVS format datetime,temperature,moisture
	
	generate plots with gnuplot
	
	
	