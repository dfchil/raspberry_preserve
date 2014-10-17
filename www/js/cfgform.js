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
                "placeholder" : d['defval'].length>0?d['defval']:" ",
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
  for(  var i = d['range'][0]; 
        i <= d['range'][1];
        i = (d['type'] == 'intrange'?i+1:parseInt(i*1.4))){
    var opt = $(document.createElement( "option"));
    opt.text(""+i + d['symbol']);
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


function new_btn(label, click){
    var lbl = $(document.createElement('label')).append(
        $(document.createElement('span')));
  
    lbl.first().append($(document.createElement('input')).attr({
        "type": "button", "class": "button", "value": label
    }).on('click', click));
    return lbl;
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
          case 'logrange':
              ncfgfrm.append(intrange_input(d));
          default:
            break;
      }
    }
  }

  ncfgfrm.append(new_btn("Apply Config", submit_cfg));

  ncfgfrm.find('#SMTP_password').parent().after(
      new_btn("Send Test Mail", test_mail));

  init_tooltips(ncfg);
  return ncfg;
}

function test_mail(){
    $('#cfgodiv').fadeOut();
    $.ajax({
      url: "cgi/mail.py",
      type: "GET",
      data: $("#cfgform").serialize(),
      dataType: "html",
    }).done(function(a_response){
        $('#cfgodiv').fadeIn();
        alert(a_response);
    });
}

function submit_cfg(){
    $.ajax({
      url: "cgi/pconfig.py",
      type: "GET",
      data: $("#cfgform").serialize(),
      dataType: "json",
    }).done(function(a_cfg){
        var tspeed = 200;
        $('#cfg_frm').replaceWith(show_cfg(a_cfg));
        $('#cfgodiv').fadeOut(tspeed).fadeIn(tspeed);
     });
}
