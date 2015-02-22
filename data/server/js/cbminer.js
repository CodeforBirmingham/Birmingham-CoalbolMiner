function get_db_config() {

}

function set_db_config() {
    
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
	    alert(r);
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
