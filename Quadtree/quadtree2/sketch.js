
let qt;
let count = 0;
/*
function setup(){
	var h=600,w=600;
	createCanvas(h,w);
	let boundary = new Rectangle(h/2,w/2,h/2,w/2);
	qt = new QuadTree(boundary, 4); 
	console.log(qt);
	for (let i=0; i < 50; i++){
		let p = new Point(Math.random() * h, Math.random() * w);
		qt.insert(p);
	}
	background(0);
	qt.show();
}
*/
/*
let qt;
let count = 0;
function setup(){
	createCanvas(400,400);
	let boundary = new Rectangle(200,200,200,200);
	qt = new QuadTree(boundary, 4);
}
function sleepFor( sleepDuration ){
    var now = new Date().getTime();
    while(new Date().getTime() < now + sleepDuration){} 
}
function draw(){
background(0);
	if (mouseIsPressed){
		sleepFor(500);
		let m = new Point(mouseX , mouseY );
		qt.insert(m)
	}
	background(0);
	qt.show();
}*/
/*
function setup(){
	createCanvas(400,400);
	let boundary = new Rectangle(200,200,200,200); //centr point and half of width and height
	qt = new QuadTree(boundary, 4); //each section just could have 4 elements
	for (let i=0; i < 300; i++){
	let p = new Point(Math.random() * 400, Math.random() * 400);
	qt.insert(p);
	}
	background(0);
	qt.show();
	stroke(0,255,0);
	rectMode(CENTER);
	let range = new Rectangle(random(200),random(200),random(50),random(50))
	rect(range.x, range.y, range.w*2,range.h*2);
	let points = [];
	qt.query(range, points,count);
	console.log(points);
	for (let p of points){
	strokeWeight(4);
	point(p.x, p.y);
	}
	console.log(count); //CANTIDAD DE VECES QUE CONSULTO
}
*/

function setup(){
	createCanvas(400,400);
	let boundary = new Rectangle(200,200,200,200); //centr point and half of width and height
	qt = new QuadTree(boundary, 4); //each section just could have 4 elements
	for (let i=0; i < 300; i++){
	let p = new Point(Math.random() * 400, Math.random() * 400);
	qt.insert(p);
	}
}
function draw(){
	background(0);
	qt.show();
	stroke(0,255,0);
	rectMode(CENTER);
	let range = new Rectangle(mouseX,mouseY,50,50)
	rect(range.x, range.y, range.w*2,range.h*2);
	let points = [];
	qt.query(range, points);
	//console.log(points);
	for (let p of points){
	strokeWeight(4);
	point(p.x, p.y);
	}
}
