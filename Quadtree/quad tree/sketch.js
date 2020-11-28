function sleep(n){
	
	var now =new Date().getTime();
	while(new Date().getTime()<now+n)
	{

	}
}

function setup(){
	createCanvas(400,400);
	let boundary = new Rectangle(200,200,200,200); //centr point and half of width and height
	qt = new QuadTree(boundary, 4); //each section just could have 4 elements
}
function draw(){
	background(0);
		if (mouseIsPressed){
		   sleep(200);
		   for (let i = 0; i < 1; i++){
			  let m = new Point(mouseX + random(-5,5), mouseY + random(-5,5));
			  qt.insert(m)
     }
  }
	background(0);
	qt.show();
}