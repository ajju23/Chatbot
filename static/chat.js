$(function() {
  var INDEX = 0;
  $("#chat-submit").click(function(e) {
    e.preventDefault();
    var msg = $("#chat-input").val();
    if(msg.trim() == ''){
      return false;
    }
    generate_message(msg, 'self');

//    msg = '';
    setTimeout(function() {
      generate_message(msg, 'user');
    }, 1000)
  })

function generate_message(msg, type) {
    INDEX++;
    var str="";
    if(msg != '' && type == 'self'){
        str += "<div id='cm-msg-"+INDEX+"' class=\"chat-msg "+type+"\">";
        str += "<span class=\"msg-avatar\">";
        str += "<\/span>";
        str += "<div class=\"cm-msg-text\" name=\"cm-msg-text\">";
        str += msg;
        str += "<\/div>";
        str += "<\/div>";
        $(".chat-logs").append(str);
    }
    if(msg!='' && type == 'user'){
        $.get("/get", { chatInput: msg }).done(function(data) {
                msg = '';
                if (data != ''){
                    str = "";
                    str += "<div id='cm-msg-"+INDEX+"' class=\"chat-msg "+type+"\">";
                    str += "<span class=\"msg-avatar\">";
                    str += "<\/span>";
                    str += "<div class=\"cm-msg-text\" name=\"cm-msg-text\">";
                    str += data;
                    str += "<\/div>";
                    str += "<\/div>";
                    $(".chat-logs").append(str);
                    data = '';
                }
              });
          }
    $("#cm-msg-"+INDEX).hide().fadeIn(300);
    $("#chat-input").val('');
    $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight}, 1000);
  }

  $(document).delegate(".chat-btn", "click", function() {
    var value = $(this).attr("chat-value");
    var name = $(this).html();
    $("#chat-input").attr("disabled", false);
    generate_message(name, 'self');
  })

  $("#chat-circle").click(function() {
    $("#chat-circle").toggle('scale');
    $(".chat-box").toggle('scale');
  })

  $(".chat-box-toggle").click(function() {
    $("#chat-circle").toggle('scale');
    $(".chat-box").toggle('scale');
  })

  $("#chat-input").keypress(function(e) {
     if(e.which == 13) {
        $("#chat-submit").click();
     }
  })
})

