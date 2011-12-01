var srbag = srbag || {};
srbag.load = srbag.load || {};
srbag.INSTA = srbag.INSTA || {};
srbag.DOODLES = srbag.DOODLES || {};
srbag.SLIDESHOW = srbag.SLIDESHOW || {};

srbag.INSTA.NUM_IMGS = 229;
srbag.INSTA.URL_L = "http://dl.dropbox.com/u/1654579/Pictures/instagram/sb_phone_";

srbag.DOODLES.NUM_IMGS = 32;
srbag.DOODLES.URL_L = "http://dl.dropbox.com/u/1654579/Pictures/doodles/sb_doodle_";

srbag.SLIDESHOW.NUM_IMGS;
srbag.SLIDESHOW.URL_L;
srbag.SLIDESHOW.SS_TYPE;

srbag.listen = function(el, evnt, func) {
    if (el.addEventListener)  {// W3C DOM 
        el.addEventListener(evnt,func,false);
    } else if (el.attachEvent) { // IE DOM
         var r = el.attachEvent("on"+evnt, func);
	     return r;
    }
};

srbag.listen(window, 'load', function() {
        srbag.setSSType();
        if (srbag.SLIDESHOW.SS_TYPE) {
            srbag.slideshowOnLoad();
        }
    }
);


// -------------- slideshow related js ---------------
srbag.setSSType = function() {
    var ss_type;
    if (window.location.pathname == "/insta") {
        srbag.SLIDESHOW.SS_TYPE = "insta";
        srbag.SLIDESHOW.NUM_IMGS = srbag.INSTA.NUM_IMGS;
        srbag.SLIDESHOW.URL_L = srbag.INSTA.URL_L;
    } else if (window.location.pathname == "/doodles") {
        srbag.SLIDESHOW.SS_TYPE = "doodles";
        srbag.SLIDESHOW.NUM_IMGS = srbag.DOODLES.NUM_IMGS;
        srbag.SLIDESHOW.URL_L = srbag.DOODLES.URL_L;
    }
};

srbag.slideshowOnLoad = function() {
    var img_number = srbag.getImageNumberFromHash();
    if (img_number) {
        srbag.setImage(img_number);
    } else {
        srbag.getAndSetRandomImage();
    }
	srbag.listenForKeyboardShortcuts();
	srbag.checkHashChange();
};

srbag.getImageNumberFromHash = function() {
    var img_number;
    try {
        if (window.location.hash) {
            var img_number_re = /^#([\d]{1,5})$/;
            var img_number_array = window.location.hash.match(img_number_re);
            if (img_number_array.length > 0) {
                img_number = img_number_array[1];
            }
        }
    } catch(zz) {}
    return (img_number) ? img_number : false;
};

srbag.getAndSetRandomImage = function() {
    var img_number = srbag.getRandomImageNumber();
    srbag.setImage(img_number);
};

srbag.setImage = function(img_number) {
    var url = srbag.createURL(img_number);
    window.location.hash = "#"+img_number;
    var el = document.getElementById('sb_img');
	if (el) {
		el.src = url;
		el.style.display = "";
	}	
};

srbag.getRandomImageNumber = function() {
    var img_number = 0;
    while (parseInt(img_number,10) === 0) {
        img_number = Math.floor(Math.random() * srbag.SLIDESHOW.NUM_IMGS);
    }
    return srbag.convertIntToString(img_number);
};

srbag.convertIntToString = function(img_number) {
    if (srbag.SLIDESHOW.SS_TYPE == "insta") {
        if (img_number < 10) { 
            img_number = "00"+img_number; 
        } else if (img_number < 100) { 
            img_number = "0"+img_number; 
        } else { 
            img_number = ""+img_number; 
        }
    } else if (srbag.SLIDESHOW.SS_TYPE == "doodles") {
        img_number = ""+img_number;
    }
	return img_number;
};

srbag.createURL = function(img_number) {
    var url = srbag.SLIDESHOW.URL_L + img_number + ".jpg";
	return url;
};

srbag.listenForKeyboardShortcuts = function() { 
    srbag.listen(window, "keyup", function(e){
        var element;
        var current_img;
        var current_int;
        if(e.target) element=e.target;
        else if(e.srcElement) element=e.srcElement;
        if(element.nodeType==3) element=element.parentNode;
        if (e.keyCode == 74 || e.keyCode == 39) { // J or RIGHT
            try {
                current_img = srbag.getImageNumberFromHash();
                if (current_img) { current_int = parseInt(current_img, 10); }
                if (current_int) {
                    var next_int = (current_int == srbag.SLIDESHOW.NUM_IMGS) ? 1 : current_int+1;
                    srbag.setImage(srbag.convertIntToString(next_int));
                } else {
                    srbag.getAndSetRandomImage();
                }
            } catch(zz) {srbag.getAndSetRandomImage();}

        } else if (e.keyCode == 75 || e.keyCode == 37) { // K or LEFT
            try {
                current_img = srbag.getImageNumberFromHash();
                if (current_img) { current_int = parseInt(current_img, 10); }
                if (current_int) {
                    var next_int = (current_int == 1) ? srbag.SLIDESHOW.NUM_IMGS : current_int-1;
                    srbag.setImage(srbag.convertIntToString(next_int));
                } else {
                    srbag.getAndSetRandomImage();
                }
            } catch(zz) {srbag.getAndSetRandomImage();}
        } else if (e.keyCode == 82) { // R
            srbag.getAndSetRandomImage();
        }
    });
};

srbag.checkHashChange = function() {
    if ("onhashchange" in window) { // event supported?
	    window.onhashchange = function () {
	        var img_number = srbag.getImageNumberFromHash();
	        if (img_number) {
	            srbag.setImage(img_number);
	        }
	    };
	}
	else { // event not supported:
	    var storedHash = window.location.hash;
	    window.setInterval(function () {
	        if (window.location.hash != storedHash) {
	            storedHash = window.location.hash;
	            var img_number = srbag.getImageNumberFromHash();
    	        if (img_number) {
    	            srbag.setImage(img_number);
    	        }
	        }
	    }, 100);
	}
};
