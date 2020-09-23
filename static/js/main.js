$(document).ready(function () {
	$('form').on('submit', function (event) {
		$.ajax({
			data: {
				client_id: $('#ClientID').val(),
				client_secert: $('#ClientSec').val(),
				redirect_uri: $('#RedirectURI').val(),
				scopes: $('#Scopes').val()
			},
			traditional: true,
			type: 'POST',
			url: '/process'
		})
		.done(function (data) {
			if (!data) {
				$('#errorAlert').text(data).show();
				$('#successAlert').hide();
			} else {
				$('#TextAreaData').val(data);
				$("#openInBrowser").attr('href', data);
				$('#successAlert').text('Open this url and grant permissons').show();
				$('#errorAlert').hide();
			}
		});
    event.preventDefault();
	});
});

$(document).ready(function () {
	$('#CopyBtn').click(function () {
		var clipboard = new Clipboard('#CopyBtn');
	});
});