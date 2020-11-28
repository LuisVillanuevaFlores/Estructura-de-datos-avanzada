
function setup(){
	var width = 250;
	var height = 200;
	createCanvas(width,height);
	background(0);
	for (var x = 0; x < width; x += width / 10) {
		for (var y = 0; y < height; y += height / 5) {
			stroke(125, 125, 125);
			strokeWeight(1);
			line(x, 0, x, height);
			line(0, y, width, y);
		}
	}
	/*var data = [
		[40,70],
		[70,130],
		[90,40],
		
		[110, 100],
		
		[140,110],
		
		[160, 100],
		
		[150, 30]
	];*/
	var data=[]
	
	var point = [140,90];
	stroke(255, 204, 0);
	strokeWeight(4);
	fill(255, 255, 255,0);
	//ellipse(point[0],height- point[1], 100, 100);
	rect(point[0]-50,height- point[1]-50,100,100)
	stroke(125, 125, 125);
	strokeWeight(1);
	for(let i = 0; i < 10; i++){
		var x = Math.floor(Math.random() * height);
		var y = Math.floor(Math.random() * height);
		data.push([x, y]);
		fill(255, 255, 255);
		circle(x, height - y, 7);
		textSize(8);
		text(x + ',' + y, x + 5, height - y);
	}
	var root = build_kdtree(data,0);
	console.log(root);
	var l=generate_dot(root);
	fill(0,255,255);
	x=point[0];
	y=point[1];
	circle(x,height-y,7);
	//var cerca=nearest2(root,point,50)
	var cerca=nearest3(root,point,100,100)
	console.log(cerca)
	fill(0,255,255);
	x=point[0];
	y=point[1];
	circle(x,height-y,7);
	for(let i = 0; i < cerca.length; i++){
		fill(255,0,255);
		x=cerca[i][1][0];
		y=cerca[i][1][1];
		circle(x,height-y,7);
	}

}
