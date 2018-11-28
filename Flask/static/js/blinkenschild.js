function update_pics()
{
   $("ul#pics").empty();
   console.log("updating pics");

   $.getJSON( "/api/pictures", function( data ) {
        $.each( data, function(x,t ) {
        console.log( t );
        $("ul#pics").append("<li><img src='static/pics/"+t+"'></li>");
        });


        $("ul#pics li img").click(function() {
                t = $(this).attr("src");
                console.log(t);
                $("#pic").val(t);

                $("#pictures").submit();
        }); // .click()

   }); // .getJson

   $("#pictures").submit(function(e){
       $.ajax({
           url: "/api/pictures",
           type: "POST",
           data: $("#pictures").serialize(),
           success: function(response){
             console.log(response);
           },
           error: function(error){
             console.log(error);
           }
        });
             
	e.preventDefault();

   });
}

$(function(){update_pics();});





function update_tweets()
{
			$("ul#tweets").empty();

			console.log("updating tweets");
					$.getJSON( "/api/twitter", function( data ) {
						    $.each( data, function(x,t ) {
							    //console.log( x );
							    $("ul#tweets").append("<li>@"+t.user+": "+ t.msg+"</li>");
							     });

							    $("ul#tweets li").click(function() {
								t = $(this).text();
								console.log(t);
								$("#tweet").val(t);

								$("#twitter").submit();
							    }); // .click()

					}); // .getJson
		 
								$("#twitter").submit(function(e){
								  $.ajax({
									url: "/api/twitter",
									type: "POST",
									data: $("#twitter").serialize(),
									success: function(response){
										console.log(response);
									},
									error: function(error){
										console.log(error);
									}
								  });
			      e.preventDefault();

        });

//setTimeout(update_tweets, 5000);
}



$(function(){update_tweets();});





$(function(){
			$("#youtube").submit(function(e){
				$.ajax({
					url: "/api/youtube",
					type: "POST",
					data: $("#youtube").serialize(),
					success: function(response){
						console.log(response);
					},
					error: function(error){
						console.log(error);
					}
				});
				e.preventDefault();
			});
});





$(function(){
			$("#text").submit(function(e){
				$.ajax({
					url: "/api/text",
					type: "POST",
					data: $("#text").serialize(),
					success: function(response){
						console.log(response);
					},
					error: function(error){
						console.log(error);
					}
				});
				e.preventDefault();
			});
});







$(function(){
			$("#pictureUploader").change(function(e){
				$.ajax({
					url: "/api/picture",
					type: "POST",
					success: function(response){
						console.log(response);
					},
					error: function(error){
						console.log(error);
					}
				});
				e.preventDefault();
			});
});






function changeHandler(files) {
			for (let i = 0, file; file = files[i]; i++) {
				if (!file.type.startsWith("image/")) {
					continue;
				}
				//upload image
				//display image from server
				let reader = new FileReader();
				reader.onload = function(event) {
					let newDatabaseString = event.target.result;
				}
				reader.readAsText(file);
			}
			return false;
}
