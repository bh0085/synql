$(init)
var groups_selector, qeo

function init(){
    groups_selector = $('<div>').appendTo($('#content')).addClass('groups_selector')
    groups_selector.append($('<div>').addClass('label_ur').text('Query Type'))
   
    qeo = $('<div>').addClass('query_expanded_options').appendTo($('#content')) 
    	.append($('<div>').text('no content to display').addClass('quiet'))
    qeo.append($('<div>').addClass('label_ur').text('Query Instance'))

    groups = $.getJSON("/demo/getQueryTypes",{},queryTypesInitialized)
    rcontainer = $('<div>').addClass('results_container').appendTo($('#content'))
    	.append($('<div>').text('no content to display').addClass('quiet'))
    rcontainer.append($('<div>').addClass('label_ur').text('Query Results'))

    ranalysis = $('<div>').addClass('projection_container').appendTo($('#content'))
	.append($('<div>').text('no content to display').addClass('quiet'))
    ranalysis.append($('<div>').addClass('label_ur').text('Query Projection, Summarization'))

    rstream = $('<div>').addClass('stream_container').appendTo($('#content'))
	.append($('<div>').text('no content to display').addClass('quiet'))
    rstream.append($('<div>').addClass('label_ur').text('Query Stream Chaining'))   

}

function queryTypesInitialized(data){
    var title, desc, infoFun, context, gs
    /**
       Displays the link bar describing the different kinds of preset queries
       that the user may run and view through the webserver.
       
       data = {
         band:{
	 title:[string]  --  display title for query type
	 description:[string] -- tooltip description for query type
	 infoFun:[string]  -- ajax function to get info for query
	 runFun:[string] -- ajax function to run the query type once opt selected
	 }, 
	 bandcollection:{...},
	 person:{...},
	 food:{...},...
    */
    


    gs = $('.groups_selector')
    gs.empty()
    gs.append($('<div>').addClass('label_ur').text('Query Type'))
    gs.append($('<div>').text('Choose a filter type to begin:'))

    for(var key in data){
	title = data[key].title
	desc = data[key].description
	infoFun = data[key].infoFun
	context = data[key]

	gs.append($("<span>")
		  .append($('<a>', {href:'#'})
			  .click($.proxy(function(){
			      $.getJSON('/demo/'+this.infoFun,
					{},
					$.proxy(queryOptsReceived,this)
				       )
			  },context))
			  .text(title)
			  .attr('title', desc)
			  .tooltip({delay:0,
				    showURL:false,
				    extraClass:'fixedwidth'})
			 ))
	    .append($('<span>').text(', '))
    }

}

function queryOptsReceived(data){
    /**
       A set of query options should idefine the field of the data object,
       "options" consisting of a list of "n" querying options for the user.
       Each of these options should define a display name for the cluster
       and a list of aliases that will be run in the expanded query.

       data:{
       options: [
       {'name': name1
       'aliases':['alias1', 'alias2',...],
       },...
       
       ]
     */
    
    
    
    

    // Group info contains information was return in the earlier call to
    // getQueryTypes for the query type that has been chosen - in particular,
    // "runFun" which will be required on item click.
    group_info = this
    qeo.empty()
    qeo.append($('<div>').addClass('label_ur').text('Query Instance'))
    qeo.append($('<div>').addClass('header').text(group_info.title + ':' ))
    
    
    if( group_info.title == 'Band Collections'){
	makePresetOptions(data, group_info)
    } else {
	makeSuggestOptions(data,group_info)
    }
    

    return
}

function makeSuggestOptions(data, group_info){
    var filter

    if(group_info.title == 'Bands'){
	filter = '(all type:/music/musical_group)'
    } else if( group_info.title == 'Foods'){
	throw 'cannot deal with query'
    } else if(group_info.title == 'People'){
	filter = '(all type:/people/person)'
    } else {
	throw "unhandled group"
    }

    qeo.append($('<input>', {id:'fb_suggest'}))
    context = {group_info:group_info}
    $("#fb_suggest")
	.suggest({filter:filter})
	.bind("fb-select", $.proxy(function(e,data){
	    params = {'name':data.name,
		      'data':JSON.stringify(data)}
	    url = '/demo/'+this.group_info.runFun
	    
	    $.getJSON(url,
		      params,
		      function(){console.log('sent out runCommand')}
		  );
	    this.item = data;
	    query_initiated(this);
	}, context));
}

function makePresetOptions(data,group_info){
    opts = data.options
    /*Display available options for selected group.*/
    for (var i in opts){
	name = opts[i].name
	aliases = opts[i].aliases
	if (aliases == null){
	    continue
	}
	/*Adds in a clickable link to run the query represented by "name

	 the callback once the stream is launched will query the server for 
	 updates a few times a second.
	 */
	context = {item:opts[i],
		   group_info:group_info}
	qdiv = $('<div>')
	    .addClass('query_optitem')
	    .addClass('listitem')
	    .append($('<a>', {href:'#'})
		    .text(name)
		    .click($.proxy(function(){
			$.post('/demo/'+this.group_info.runFun,
			       {'name':this.item.name});
			query_initiated(this);
		    }, context)))
	    .append($('<span>').text(' - '))
	    .append($('<span>').text(aliases.join(', '))
		    .addClass('query_aliaseslist'))
	    .appendTo(qeo)
    }
}

var status_interval;
function query_initiated(data){
    /**
       Data describes query params and state.

       data = {
       item:{name:[string],
             aliases:[[string],[string],...]},
       group_info:{[input to queryOptsReceived]}
       }
     */
    $('#content').find('.results_container').empty()
    
    rcontainer.append($('<div>').addClass('label_ur').text('Query Results'))
    qsummary = $('<div>').addClass('query_summary').appendTo(rcontainer)
    qsummary.append($('<div>').addClass('query_status'))
    qsummary.append($('<div>').addClass('query_params'))
    qresults = $('<div>').addClass('query_results').prependTo(rcontainer)

    qresults.append($('<div>').addClass('header')
		    .text(data.item.name))
    qresults.append($('<div>').addClass('list').addClass('query_results_items'))
    $('.query_results_items')
	.append($('<div>').text('...no results yet'))
    
    
    
    context = data
    makeProjectionOptions(data)
    status_interval = window.setInterval(
	$.proxy(function(){
	    $.getJSON('/demo/checkStatus',
		      {},
		      $.proxy(onStatusChecked,this))
	},context),1000)
   
    
}

var aliasColors = null;
function makeProjectionOptions(data){

    
    ranalysis = $('.projection_container').empty()
    ranalysis.append($('<div>').addClass('label_ur').text('Query Projection, Summarization'))

    ranalysis.append($('<div>').text('Aliases generated for query" '+ data.name+'"')) 

    name = data.name
    
    
    console.log('Data!', data)
    aliases = ['barack', 'obama','potus','barry','Barack Obama'] //data.aliases
    aliasColors = []
    for( var i = 0 ; i <  aliases.length ; i++){
	color=get_random_color()
	aliasColors.push(color)
	a = aliases[i]
	ranalysis.append($('<span>').css('color', color).text(a))
    }

    
}

function get_random_color() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.round(Math.random() * 15)];
    }
    return color;
}

function query_halted(){
    if (status_interval == null){
	throw 'status interval apparently unset'
    }
    window.clearInterval(status_interval)
    //window.clearInterval(citiesInterval)
    status_interval = null
    
}

function onStatusChecked(data){
    init_data = this
  

    if (data.params.name != init_data.item.name){
	console.log('waiting for the proper params file')
    }

    if(citiesInterval ==null){
	citiesInterval =  window.setInterval(addCity,50)
    }

    if (data.status == 'finished'){
	$('.query_status')
	    .empty()
	    .append($('<div>').text('done!').css('color', 'red'))
	query_halted();
    }else {
	$('.query_status')
	    .empty()
	    .append($('<div>').addClass('field')
		    .append($('<span>').addClass('field_label').text('Status: '))
		    .append($('<span>').addClass('field_content').text(data.status))
		   )
    }

    
    $('.query_params')
	.empty()
	.append($('<div>').addClass('field')
		.append($('<span>').addClass('field_label').text('Params: '))
		.append($('<span>').addClass('field_content')
			.html('<br/>'+
			    $.map(data.params,
				  function(i,e){
				      tval = String(e) + ': ' + $('<span>').text(String(i)).css('color','gray').html() 
				      return $('<span>').text(tval).html();
				  }).join('<br/>')))
	       )

    $('.query_results')
	.empty()
    for (var i = 0 ; i < data.tweets.length; i++){
	$('.query_results')
	    .append($('<div>').addClass('listitem')
		    .text(data.tweets[i]))
    }
    
}