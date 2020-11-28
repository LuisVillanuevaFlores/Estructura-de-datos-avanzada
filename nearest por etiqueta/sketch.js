
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
	var data = [
		[40,70],
		[70,130],
		[90,40],
		[110, 100],
		[140,110],
		[160, 100],
		[150, 30]
	];
	
	var point = [140,90];
	/*for(let i = 0; i < 12; i++){
		var x = Math.floor(Math.random() * height);
		var y = Math.floor(Math.random() * height);
		data.push([x, y]);
		fill(255, 255, 255);
		circle(x, height - y, 7);
		textSize(8);
		text(x + ',' + y, x + 5, height - y);
	}
	*/
	//var best=[1000,1000];
	var root = build_kdtree(data,0);
	console.log(root);
	/*
	var h = getHeight(root);
	console.log(h);
	*/
	var l=generate_dot(root);
	console.log(l);
	/*
	console.log(closest_point_brute_force(data, point))
	console.log(naive_closest_point(root, point, 0));
	console.log(naive_closest_point2(root, point, 0));
	console.log(closest_point(root, point, 0));
	*/
	//console.log(nearest(root, point, 3));
	console.log("---------------------------");
	console.log(closest_point(root,point));
	console.log("A");
	console.log(nearest(root,point,4));


}
