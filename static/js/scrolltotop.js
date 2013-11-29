/*
jQuery Scroll To Top Plugin
Appends a link allowing you to go back to the top of the page after you've scrolled down a certain distance
version 1
copyright NOE Interactive
*/
(function($, $w) {
	"use strict";
    $.fn.backtotop = function(options) {

		//Options
		var settings = {
			topAnchor : 'body', //Selector of the element you want to reach when you go back up
            topOffset : 100, //Distance from the top the body has to travel to reveal the back to top button
			      animationSpeed: 1000, //The speed of the animation to go back to top
            animationEase: 'swing', //The easing function used for the animation
            bckTopLinkTitle: '', // Link Title
            bcktitle: 'Back To Top',
            bckTopLinkClass : 'backTopLink' //Link Class
		};

		options && $.extend(settings, options);

		//We store all the selectors we are going to need
		var $bckTop = $(this),
		$b = $('html,body'),
		isVisible = false,
		$topAnchor = $(settings.topAnchor),
		//Link creation
        $bckTopLink = $('<a>', {'class' : settings.bckTopLinkClass+' backtotopinstance', title : settings.bcktitle, text : settings.bckTopLinkTitle})
        				.appendTo($bckTop)
                        .hide()
        				.click(function(e) {
        					e.preventDefault();
    	                    $b.animate({scrollTop: $topAnchor.position().top},settings.animationSpeed,settings.animationEase);
	                        return false;
        				});

        $w.scroll(_sc);
        _sc();//First launch without scroll

        function _sc(){
           var scrollTop = $w.scrollTop();
           if(scrollTop > settings.topOffset && !isVisible) { //Is the link visible?
               //No -> show it
                $bckTopLink.stop().fadeIn('slow');
                isVisible = true;
           } else if(scrollTop <= settings.topOffset && isVisible) {
               //Yes -> hide it
                    $bckTopLink.stop().fadeOut('slow');
                isVisible = false;
           }
        }

    }

})(jQuery, jQuery(window));