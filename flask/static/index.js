window.onload = () => {
    var boxwidth = document.getElementById('leftbox').clientWidth;
    document.getElementById('leftbox').setAttribute("style","height:"+parseInt(boxwidth*0.75,10)+"px");
    document.getElementById('rightbox').setAttribute("style","height:"+parseInt(boxwidth*0.75,10)+"px");
	$('#sendbutton').click(() => {
		imagebox = $('#imagebox1')
		input = $('#imageinput')[0]
        var leftimgsrc = document.getElementById("imagebox").getAttribute("src");
        
        document.getElementById("rightboxtext").innerHTML="Grabing...";
		if(input.files && input.files[0])
		{
			fetch(leftimgsrc)
				.then(res => res.blob())
				.then(blob => {
					const file = new File([blob], "capture.jpg", {
						type: 'image/jpeg'
					});

			let formData = new FormData();
			//formData.append('image' , input.files[0]);
			formData.append('image' , file);
			$.ajax({
				url:"/docseg",
				type:"POST",
				data: formData,
				cache: false,
				processData:false,
                timeout: 60000,
				contentType:false,
				error: function(data){
					console.log("upload error" , data);
					console.log(data.getAllResponseHeaders());
				},
				success: function(data){
					// alert("hello"); // if it's failing on actual server check your server FIREWALL + SET UP CORS
                    document.getElementById("rightboxtext").innerHTML="";
					bytestring = data['status']
					image = bytestring.split('\'')[1]
                    //console.log(image)
					imagebox.attr('src' , 'data:image/png;base64,'+image)
                    var boxwidth = document.getElementById('leftbox').clientWidth;
                    var boxheight = document.getElementById('leftbox').clientHeight;
                    //var boxwidth = document.getElementById('leftbox').width;
                    //var boxheight = document.getElementById('leftbox').height;
                    imagebox.height(boxheight);
                    imagebox.width(boxwidth);
                    imagebox.attr('style','visibility:visible'); 
				}
			});
		  });
		}
	});
};



function readUrl(input){
	imagebox = $('#imagebox')
	imagebox1 = $('#imagebox1')
    leftbox = $('#leftbox')
    rightbox = $('#rightbox')
	console.log("evoked readUrl")
	if(input.files && input.files[0]){
		let reader = new FileReader();
		reader.onload = function(e){
			// console.log(e)
            var image = new Image();
            image.src = e.target.result;

            image.onload = function(){
                imgWidth = this.width
                imgHeight = this.height
                var boxwidth = document.getElementById('leftbox').clientWidth;
                var boxheight = parseInt((imgHeight/imgWidth)*boxwidth)
                leftbox.height(boxheight)
                leftbox.width(boxwidth)
                rightbox.height(boxheight)
                rightbox.width(boxwidth)
                imagebox.height(boxheight);
                imagebox.width(boxwidth);
                imagebox1.height(boxheight);
                imagebox1.width(boxwidth);

                const elem = document.createElement('canvas');
                elem.width = boxwidth;
                elem.height = boxheight;
                const ctx = elem.getContext('2d');
                // img.width and img.height will contain the original dimensions
                ctx.drawImage(image, 0, 0, boxwidth, boxheight);
                
                //ctx.canvas.toBlob((blob) => {
                //    const file = new File([blob], input.files[0].name, {
                //        type: 'image/jpeg',
                //        lastModified: Date.now()
                //    });
                //}, 'image/jpeg', 1);

                //const data = ctx.canvas.toDataURL(image)
                const data = ctx.canvas.toDataURL(input.files[0].type)
                
                //imagebox.attr('src',this.src); 
                imagebox.attr('src',data); 
                document.getElementById("leftboxtext").innerHTML="";
                //imagebox1.attr('src',''); 
                imagebox1.attr('style','visibility:hidden'); 
                //console.log(data)
            }
		}
		reader.readAsDataURL(input.files[0]);
	}

	
}
