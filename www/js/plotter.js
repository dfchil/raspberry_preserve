function getISODateTime(d){
  // padding function
  var s = function(a,b){return(1e15+a+"").slice(-b)};

  // default date parameter
  if (typeof d === 'undefined'){
      d = new Date();
  };

  // return ISO datetime
  return d.getFullYear() + '-' +
      s(d.getMonth()+1,2) + '-' +
      s(d.getDate(),2) + ' ' +
      s(d.getHours(),2) + ':' +
      s(d.getMinutes(),2);
}

function replot(a_origin, a_begin, a_end, a_width, a_height){
    var origin = a_origin ? "&origin="+a_origin : "" ;
    var begin = a_begin || $('#begin').data('datetimepicker').getLocalDate();
    var end =   a_end || $('#end').data('datetimepicker').getLocalDate();


    var firstdate = new Date(min_secs()+ begin.getTimezoneOffset());
    if (begin < firstdate){
      begin = firstdate;
    }
      
    var width = parseInt(a_width || $('#outerframe').width() , 10);
    var height = parseInt(a_height || $( window).height() *0.7 , 10);
    var url = encodeURI('cgi/plotter.py?begin=' + getISODateTime(begin) +
                                        "&end="+getISODateTime(end) +
                                        "&width="+width+
                                        "&height="+height+
                                        origin);
                                        
    var nsvg = $(document.createElement('object'));
    nsvg.attr({ "id":"svg1", 
                "type":"image/svg+xml",
                'width' : width+20, 
                'height': height+20,
                'data':  url });
    // $("#tabs1-data").append(nsvg);
    $('#svg1').replaceWith(nsvg);
}

function show_range(){
  $( "#tabs1-data").find( "span" ).first().text(
                        "Datapoints from: "+ 
                        getISODateTime(new Date(min_secs()))+ " to: "+
                        getISODateTime(new Date(max_secs())));
}

function  set_time_pickers(begintime, endtime){
  $('#begin').data('datetimepicker').setLocalDate(new Date(begintime));
  $('#end').data('datetimepicker').setLocalDate(new Date(endtime));  
  $('#end').data('datetimepicker').setEndDate(new Date(max_secs()));
}

$(document).ready( function() {
  $('#tab-container').easytabs();
  
  var endtime = max_secs();
  var begintime = endtime - 60*60*1000 * default_begin();

  var options = {
      pickSeconds: false,
      format: 'yyyy-MM-dd hh:mm',
      endDate: new Date(max_secs()),
      startDate: new Date(min_secs()),
  }
  $('#begin_val').attr("data-format", options['format']);
  $('#end_val').attr("data-format", options['format']);
  $('i').each(function(){
      $(this).attr("data-time-icon","icon-time");
      $(this).attr("data-date-icon","icon-calendar");
  });

  $('#begin').datetimepicker(options);
  $('#end').datetimepicker(options);

  set_time_pickers(begintime, endtime);

  $( ".date" ).on( "changeDate", function(tevent) {
      $.doTimeout( 'svgreload', 300, function(){
         tevent = tevent || window.event;
          replot(tevent.target.id);}, true);
      });

  $( window ).resize(function() {
      $.doTimeout( 'svgreload', 300, function(){
          replot();
          }, true); 
      });
  $("#tabs1-cfg").append(show_cfg());
  replot();
});