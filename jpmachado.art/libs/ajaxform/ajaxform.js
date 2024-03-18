/*==============================
    5. Ajax Form
==============================*/
$('#ajaxFormSubmit').on('click',function(){
    var Form = $('#ajaxForm');
    var hasErrors = Form.validator('validate').has('.has-error').length
    if (hasErrors){
        
    }else{
        $('#fullscreenloading').show();
        $('#boxedResult').show();
        $('#sendResult').html('<div class="uil-rolling-css"><div><div></div><div></div></div></div>');
        $.ajax({
            type: 'POST',
            url: 'send_form.php',
            data: Form.serialize(),
            success: function(msg){
                $('#sendResult').html(msg)
            },
            error: function(){
                $('#sendResult').html('<img src="libs/ajaxform/form-icon-error.png"/><br/><span class="title error">Sorry!</span><br/>Your data has not been sent. Please try again.<br /><strong>Error: #AJ001</strong><br /><br /><button class="btn btn-default BtnCloseResult" type="button">Close</button>');
            }
        });
    }
});
$(document).on('click', '.BtnCloseResult', function () {
    $('#boxedResult').hide();
    $('#fullscreenloading').hide();
});

