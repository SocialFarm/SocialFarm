function _init_carousel(carousel) {
	$('#slider .next').bind('click', function() {
		carousel.next();
		return false;
	});
	
	$('#slider .prev').bind('click', function() {
		carousel.prev();
		return false;
	});
};



$(document).ready(function() {
	$("#slider-holder").jcarousel({
		scroll: 1,
		auto: 5,
		wrap: 'both',
		initCallback: _init_carousel,
		buttonNextHTML: null,
		buttonPrevHTML: null
	});
});
