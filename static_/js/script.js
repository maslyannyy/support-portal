$(function() {
	$('.form-btn').click(function() {
		let buttonWidth = $(this).width();
		$('.btn').prop('disabled', true);
		$('.btn').empty().append('<div class="spinner-border spinner-border-sm" role="status"></div>').width(buttonWidth);
		$('form').submit();
		return false	
	});
});

$(function() {
	$('.swith-btn').click(function() {
		let taskId = $(this).val();
		let button = $(this);
		let buttonText = button.text();
		$.ajax({
			url: '/tasks/switch/',
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json'
			},
			data: JSON.stringify({
				id: taskId
			}),
			dataType : 'json',
			beforeSend: function() { 
				let buttonWidth = button.width();
				$('.btn').prop('disabled', true);
				button.empty().append('<div class="spinner-border spinner-border-sm" role="status"></div>').width(buttonWidth);
			},
			success: function(response) {
				if (response['success']) {
					setTimeout(function() {
						if (response['is_active'] == true) {
							button.empty().text('Остановить').width('auto');
						} else {
							button.empty().text('Запустить').width('auto');
						}
						$('.btn').prop('disabled', false);
					}, 300);
				}
			},
			error: function(response) {
				console.log(response);
				setTimeout(function() {
					button.empty().text(buttonText);
					$('.btn').prop('disabled', false);
				}, 300);
			}
		});
	});
});

$(function() {
    $('.sync-btn').click(
		function() {
			let url = $(this).parent().find('input').val();
			var button = $(this);
			let buttonText = button.text();
			$.ajax({
				url: url,
				type: 'POST',
				beforeSend: function() { 
					let buttonWidth = button.width();
					$('.btn').prop('disabled', true);
					button.empty().append('<div class="spinner-border spinner-border-sm" role="status"></div>').width(buttonWidth);
				},
				success: function(response) {
					if (!response['success']) {
						console.log(response);
					}
					setTimeout(function(){
						$('.btn').prop('disabled', false);
						button.empty().text('Запустить');
					}, 300);
				},
				error: function(response) {
					console.log(response);
					setTimeout(function() {
						button.empty().text(buttonText);
						$('.btn').prop('disabled', false);
					}, 300);
				}
			 });
			return false; 
		}
	);
});
