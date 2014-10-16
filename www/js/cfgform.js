function text_input(d){
  var nlabel = $(document.createElement( "label" )).addClass(
          'masterTooltip').attr("title" ,d['description']);
  var nspan = $(document.createElement( "span" )).text(d['label']+ " :");


  if (d['type'] == "largetxt"){
    var ninput = $(document.createElement( "textarea" ));
    ninput.text(d['value']);
  }
  else{
    var ninput = $(document.createElement( "input" ));
    ninput.attr("type", d['type']);
    ninput.val(d['value']);
  }

  ninput.attr({'id' : d['key'], 
                'name' : d['key'],
                "placeholder" : d['defval'],
              });
  nlabel.append(nspan);
  nlabel.append(ninput);
  return nlabel;
}

function intrange_input(d){
  var nlabel = $(document.createElement( "label" )).addClass(
          'masterTooltip').attr("title" ,d['description']);
  var nspan = $(document.createElement( "span" )).text(d['label']+ " :");
  var nselect = $(document.createElement( "select" ));
  nselect.attr({'id' : d['key'], 
                'name' : d['key']
              });
  for(var i = d['range'][0]; i < d['range'][1]; i++){
    var opt = $(document.createElement( "option"));
    opt.text(""+i);
    opt.val(""+i);
    if (i == d['value'])
      opt.prop('selected', true);
    nselect.append(opt);
  }
  nlabel.append(nspan);
  nlabel.append(nselect);
  return nlabel;
}

function init_tooltips(outerelement){
    // Tooltip only Text
    outerelement.find('.masterTooltip').hover(function(){
        // Hover over code
        var title = $(this).attr('title');
        $(this).data('tipText', title).removeAttr('title');
        $('<p class="simpletooltip"></p>')
        .text(title)
        .appendTo('body')
        .fadeIn('slow');
        }, function() {
                // Hover out code
                $(this).attr('title', $(this).data('tipText'));
                $('.simpletooltip').remove();
        }).mousemove(function(e) {
                var mousex = e.pageX + 20; //Get X coordinates
                var mousey = e.pageY + 10; //Get Y coordinates
                $('.simpletooltip')
                .css({ top: mousey, left: mousex })
        });
}

function show_cfg(a_cfg){
  var cfgdata = a_cfg || config_json();
  var ncfg = $(document.createElement('div')).addClass("white-pink").
      attr("id", "cfg_frm");
  
  var nch1 = $(document.createElement('h1')).text("System Configuration");
  nch1.append($(document.createElement('span')).text('Further configuration options available in the rb_preserve.cfg file'));
  ncfg.append(nch1);

  var ncfgodiv = $(document.createElement('div')).attr("id", "cfgodiv");
  var ncfgfrm = $(document.createElement('form')).attr("id", "cfgform");
  ncfgodiv.append(ncfgfrm);
  ncfg.append(ncfgodiv);

  for (var i = 0; i < Object.keys(cfgdata).length; i++){
    var d = cfgdata[""+i];

    if (d['webconfigurable']){
      switch(d['type']) {
          case 'smalltxt':
            d['type'] = 'text';
          case 'email':
          case 'password':
          case 'largetxt':
              ncfgfrm.append(text_input(d));
              break;
          case 'intrange':
              ncfgfrm.append(intrange_input(d));
          default:
            break;
      }
    }
  }
  
  ncfg.append(document.createElement('label'));
  ncfg.first().append(document.createElement('span'));
  
  var abtn = $(document.createElement('input')).attr({
      "type": "button", "class": "button", "value": "Apply"
  }).on('click', function(){submit_cfg();});
  ncfg.first().append(abtn);
  
  init_tooltips(ncfg);
  return ncfg;
}

function submit_cfg(){
    $.ajax({
      url: "pconfig.py",
      type: "POST",
      data: $("#cfgform").serialize(),
      dataType: "json",
    }).done(function(a_cfg){
         $('#cfg_frm').replaceWith(show_cfg(a_cfg));
     });
}
