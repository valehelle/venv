$(document).ready(function() {
	$(".item").click(function(event){
		var $div = $(this).next();
		var $a = $($div).find("a");
		$a.trigger('click');
	});
				
	$(document).ready(function() {
		$(".fancybox-thumb").fancybox({
			prevEffect	: 'none',
			nextEffect	: 'none',
			helpers	: {
				title	: {
					type: 'outside'
				},
				thumbs	: {
					width	: 500,						
					height	: 500
				}
			}
		});
	});

});