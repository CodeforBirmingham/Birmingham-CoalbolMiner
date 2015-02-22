function get_db_config(f) {
    console.log("get config");
    $.ajax({
	url: "/config/database",
	type: 'GET',
	success: function(r) {
	    f(r);
	}
    });
}

function set_db_config(f) {
    
}

function upload_schema(form) {
    var data;
    data = new FormData(form);

    $.ajax({
	url: '/submit/schema',
	data: data,
	processData: false,
	type: 'POST',
	contentType: false,
	success: function(r) {
	    
	}
    });
    
}

function upload_table(form) {
    var data;
    data = new FormData(form);

    $.ajax({
	url: '/submit/data',
	data: data,
	processData: false,
	type: 'POST',
	contentType: false,
	success: function(r) {

	}
    });
}
