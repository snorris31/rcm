/*$(document).ready(function () {
    $('.collapse').on('show.bs.collapse', function () {
      $('.collapse.in').collapse('hide');
    });
});
var alreadyCalled = [];
      var dropdown = {
        project: $('#projects'),
        release: $('#releases')
      }
      function updateReleases() {
        var project = dropdown.project.val();
        console.log(project);
        if (project.length) { 
          dropdown.release.empty();
    dropdown.release.append(
    $('<option>', {
        value: '', 
        text: 'Select Release'
    })
  );
          $.getJSON("{{url_for('routeRelease')}}", {project: project}, function(data) {
              console.log(data);
              data.forEach(function(item) { 
                dropdown.release.append(
                  $('<option>', {
                      value: item.id, 
                      text: item.name
                  })
                );
              });
              dropdown.release.removeAttr('disabled');
        });
      }
    }
      dropdown.project.on('change', function() {
            updateReleases();
        });
      function clickedDetails(button) {
          if (!(button in alreadyCalled)) {
            console.log(button);
            var detailsButton = button.replace('_', '.').replace('_','.');
      console.log(detailsButton);
            $.getJSON("{{url_for('routePR')}}", {detailsButton: detailsButton}, function(data) {
      console.log(data.length)
      var html;
      var html2;
      if (data[0]) { 
    html += "<th class = 'info'> PR Number </th><th class = 'info'>Responsible </th><th class = 'info'> State </th><th class = 'info'> Synopsis </th><th class = 'info'></th>"
        $(".thisone" + "." + button).append(html);
              for (var i = 0; i < data.length; i++) {
                  html2 += '<tr class = "thisone ' + button + '"><td class = "info"><a href ="https://gnats.juniper.net/web/default/' + 
      data[i].pr_number + '"> ' + data[i].pr_number + 
      "</a></td><td class = 'info'>" + data[i].responsible +"</td><td class = 'info'>" + data[i].pr_state + "</td><td class = 'info'>" + data[i].synopsis + "</td><td class = 'info'></td></tr>";
        $(".thisone" + "." + button).last().after(html2);
        $("."+ button).addClass("collapse in");
        html2 = '';
            }
    $(".thisone" + "." + button).append("</div>");
          }
          });
            alreadyCalled[button] = 1;
          } else {
      console.log("hi");
            return;
          }
      }
  
  $(document).ready(function () {
   $("input[name='compare']").change(function () {
      var maxAllowed = 2;
      var cnt = $("input[name='compare']:checked").length;
      if ((cnt > maxAllowed)) 
      {
         $(this).prop("checked", "");
         alert('Select ' + maxAllowed + ' Builds!');
      }
      });
  });
      function showDiff() {
          var html = '<li id = "builds"> <b> Comparing Builds: </b>';
    var twoBuilds = '';
    var counter = 0;
          $(':checkbox:checked').each(function(i){
            html += $(this).val() + " ";
      twoBuilds += $(this).val() + " ";
            console.log($(this).val());
      counter++;
      var html2 = '';
      var htmlremoved = '';
      if (counter == 2) { 
    $.getJSON("{{url_for('cmComparison')}}", {twoBuilds: twoBuilds}, function(data) {
    console.log(data.data[0]);
    console.log(data.data[1]);
    $("#compare2builds ul").append(html);
    $('<ul />').appendTo('#compare2builds #builds');
    var looprepos = 0;
    console.log(data.data[2].length)
    console.log(data.data[0].length)
    console.log(data.data[1].length)
          var end = (data.data[0].length + data.data[1].length) - 1;
    for(var i = 0; i < data.data[0].length; i++) {
      console.log(data.data[0].length);   
      html2 += "<li class = 'green'>" + data.data[0][i] + "</li>";
      console.log(html2);
      $("#compare2builds #builds ul").append(html2);
      html2 = '';
      looprepos++;
      console.log(looprepos);
      if (looprepos == end) {
      $('#compare2builds').jstree( {
                  "core": {
                    "themes":{
                    "icons":false
        }
        }
                  });
      }
              }
    for (var i = 0; i < data.data[1].length; i++) {
      htmlremoved += "<li class = 'red'>" + data.data[1][i] + "</li>";
      $("#compare2builds #builds ul").append(html2);
      html2 = '';
      looprepos++;
      console.log(looprepos);
      if (looprepos == end) {
      $('#compare2builds').jstree( {
                  "core": {
                    "themes":{
                    "icons":false
        }
        }
                  });
     } 
        }
    if (looprepos == end) {
      $('#compare2builds').jstree( {
                  "core": {
                    "themes":{
                    "icons":false
        }
        }
                  });
      }
    });
      }
        });
        //$("#buildnames").append(html);
        document.getElementById("diffs").style.display = "block";

      }
      function hideJumbo() { 
        document.getElementById("diffs").style.display = "None";
      }

        $(document).ready(function(){
    $('[data-toggle="popover"]').popover();   
});
*/
$(document).on('load', function() {

  $('#comparison').click(function() {
    var html = '<li id = "builds"> <b> Comparing Builds: </b>';
    var twoBuilds = '';
    var counter = 0;
    $(':checkbox:checked').each(function(i){
      html += $(this).val() + " ";
      twoBuilds += $(this).val() + " ";
            console.log($(this).val());
      counter++;
      var html2 = '';
      var htmlremoved = '';
      if (counter == 2) { 
    $.getJSON("{{url_for('cmComparison')}}", {twoBuilds: twoBuilds}, function(data) {
    console.log(data.data[0]);
    console.log(data.data[1]);
    $("#compare2builds ul").append(html);
    $('<ul />').appendTo('#compare2builds #builds');
    var looprepos = 0;
    console.log(data.data[0].length)
    console.log(data.data[1].length)
          var end = (data.data[0].length + data.data[1].length) - 1;
    for(var i = 0; i < data.data[0].length; i++) {
      console.log(data.data[0].length);   
      html2 += "<li class = 'green'>" + data.data[0][i] + "</li>";
      console.log(html2);
      $("#compare2builds #builds ul").append(html2);
      html2 = '';
      looprepos++;
      console.log(looprepos);
      if (looprepos == end) {
      $('#compare2builds').jstree( {
                  "core": {
                    "themes":{
                    "icons":false
        }
        }
                  });
      }
    }
    for (var i = 0; i < data.data[1].length; i++) {
      htmlremoved += "<li class = 'red'>" + data.data[1][i] + "</li>";
      $("#compare2builds #builds ul").append(html2);
      html2 = '';
      looprepos++;
      console.log(looprepos);
      if (looprepos == end) {
      $('#compare2builds').jstree( {
                  "core": {
                    "themes":{
                    "icons":false
        }
        }
                  });
     } 
    }
    if (looprepos == end) {
      $('#compare2builds').jstree( {
                  "core": {
                    "themes":{
                    "icons":false
        }
        }
                  });
      }
    });
      }
        });
        //$("#buildnames").append(html);
        document.getElementById("diffs").style.display = "block";
  });
      $('.collapse').on('show.bs.collapse', function () {
        $('.collapse.in').collapse('hide');
      });
  
   $("input[name='compare']").change(function () {
      var maxAllowed = 2;
      var cnt = $("input[name='compare']:checked").length;
      if ((cnt > maxAllowed)) 
      {
         $(this).prop("checked", "");
         alert('Select ' + maxAllowed + ' Builds!');
      }
      });

});
