$(initialize_gmaps);
var geocoder;
var map;
function initialize_gmaps() {
    geocoder = new google.maps.Geocoder();
    var myOptions = {
	zoom:3,
	center: new google.maps.LatLng(36,-100),
	mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    mapstyles = [
	{
	    featureType: "road",
	    stylers: [
		{ visibility: "off" }
	    ]
	},{
	    featureType: "poi",
	    stylers: [
		{ visibility: "off" }
	    ]
	},{
	    featureType: "administrative",
	    stylers: [
		{ visibility: "off" }
	    ]
	},{
	    featureType: "administrative.locality",
	    stylers: [
		{ visibility: "off" }
	    ]
	},{
	    featureType: "poi",
	    stylers: [
		{ visibility: "off" }
	    ]
	},{
	    featureType: "water",
	    stylers: [
		{ visibility: "simplified" },
		{ lightness: -62 },
		{ saturation: -63 },
		{ gamma: 0.97 }
	    ]
	},{
	}
    ]
    myOptions.styles = mapstyles;
    

   map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
   var time = new Date().getTime();
   //var ctaLayer = new google.maps.KmlLayer('http://marcua.csail.mit.edu:8000/temperatures/display?'+time,{preserveViewport: true})
   //ctaLayer.setMap(map);
    $.getJSON('/demo/cityLLs',
	      {},
	      cityLLsReceived)

 } 
var circles, cityData, cityCount;
cityCount = 0;
var citiesInterval = null;
function cityLLsReceived(data){
    cityData = data;
    circles = []
}
function addCity(){
    names = $.map(cityData,function(e,i){return i}).sort()
    
    name = names[cityCount]
    cityCount+= 1
    if (cityCount >= names.length){cityCount = 0}

    
    

    if (aliasColors == null){
	return
    }
    cidx = Math.floor(Math.random() * aliasColors.length);
    var populationOptions = {
	    strokeColor: aliasColors[0],
	    strokeOpacity: 0.8,
	    strokeWeight: 3,
	    fillColor: "#999",
	    fillOpacity: 0,
	    map: map,
	    center: new google.maps.LatLng(cityData[name].lat, -1 *cityData[name].lon),
	radius: 50000*2 * Math.random()
    };
    cityCircle = new google.maps.Circle(populationOptions);	
    circles.push(cityCircle)
    if (circles.length > 6){
	doKill = circles.splice(0,1)[0]
	doKill.setMap(null)
    }
}

