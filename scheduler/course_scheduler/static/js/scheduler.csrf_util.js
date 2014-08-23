function crsfSafeMethod(method) {
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function initializeCSRF() {
	var csrftoken = $.cookie('csrftoken');
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!crsfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});
}