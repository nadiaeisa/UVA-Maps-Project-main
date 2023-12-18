// *  References
// *  Title: Python Django Application Walkthrough Tutorial for Google Maps
// *  Author: Did Coding
// *  Date: 4/2/2021
// *  Code version: Django==3.1.7
// *  URL: https://www.youtube.com/watch?v=wCn8WND-JpU
// *  Software License: N/A

function DirectionsToggle(){
    var el = $('#dir-toggle');
    var dir_table = $('#dir-table')
    if (dir_table.attr("hidden") == "hidden") {
      dir_table.fadeIn()
      dir_table.removeAttr("hidden")
      el.html('hide <a href="javascript:void(0)" onclick="DirectionsToggle()">here')
    } else {
      dir_table.fadeOut()
      dir_table.attr("hidden", "hidden")
      el.html('click <a href="javascript:void(0)" onclick="DirectionsToggle()">here')
    }
  }