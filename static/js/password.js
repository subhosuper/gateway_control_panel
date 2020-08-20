
$(document).ready(function(){
      $('#password, #confirm_password').on('keyup', function () {
      if ($('#password').val() != $('#current_password').val() && $('#current_password').val() != $('#confirm_password').val()) {
        $('#btnSubmitDisabled').attr("disabled", false);

        if ($('#password').val() == $('#confirm_password').val()) {
          // $('#message').html('Matching').css('color', 'green');
          $('#btnSubmitDisabled').attr("disabled", false);
          $('#message').html('');
        } else {
          $('#message').html('Password not matching').css('color', 'red');
          $("#btnSubmitDisabled").attr("disabled", true);
          // $('#btnSubmitDisabled').removeAttr("disabled");
        }

      } else {
        $('#btnSubmitDisabled').attr("disabled", true);
        $('#message').html('Set different password').css('color', 'green');

      }
    });
    
});