
class Point{
	constructor(x, y, userData){
		this.x = x;
		this.y = y;
		this.userData = userData;
	}
}
class Rectangle{
	constructor(x, y, w, h){
		this.x = x; 
		this.y = y;
		this.w = w; 
		this.h = h; 
	}
	contains(point) {
	    return (point.x >= this.x - this.w &&
	      point.x <= this.x + this.w &&
	      point.y >= this.y - this.h &&
	      point.y <= this.y + this.h);
	  }
	intersects(range) {
	    return !(range.x - range.w > this.x + this.w ||
	      range.x + range.w < this.x - this.w ||
	      range.y - range.h > this.y + this.h ||
	      range.y + range.h < this.y - this.h);
	  }
}
class QuadTree{
constructor(boundary, n){
	this.boundary = boundary
	this.capacity = n;
	this.points = []; 
	this.divided = false;
}

subdivide(){
	var no=new Rectangle(
		this.boundary.x-this.boundary.w/2,
		this.boundary.y-this.boundary.h/2,
		this.boundary.w/2,
		this.boundary.h/2);
	var ne=new Rectangle(
		this.boundary.x+this.boundary.w/2,
		this.boundary.y-this.boundary.h/2,
		this.boundary.w/2,
		this.boundary.h/2);
	var so=new Rectangle(
		this.boundary.x-this.boundary.w/2,
		this.boundary.y+this.boundary.h/2,
		this.boundary.w/2,
		this.boundary.h/2);
	var se=new Rectangle(
		this.boundary.x+this.boundary.w/2,
		this.boundary.y+this.boundary.h/2,
		this.boundary.w/2,
		this.boundary.h/2);
	this.sonNO = new QuadTree(no, this.capacity);
	this.sonNE = new QuadTree(ne, this.capacity);
	this.sonSO = new QuadTree(so, this.capacity);
	this.sonSE = new QuadTree(se, this.capacity);
	this.divided=true;
}
insert(point){
	if(!this.boundary.contains(point))
		return;
	if(this.points.length<this.capacity)
		this.points.push(point);	
	else{
		if(!this.divided)
			this.subdivide();
		this.sonNO.insert(point);
		this.sonNE.insert(point);
		this.sonSO.insert(point);
		this.sonSE.insert(point);
	}
}
show(){
	stroke(255);
	strokeWeight(1);
	noFill();
	rectMode(CENTER);
	rect(this.boundary.x,this.boundary.y,this.boundary.w*2,this.boundary.h*2);
	if(this.divided){
		this.sonNO.show();
		this.sonNE.show();
		this.sonSO.show();
		this.sonSE.show();
	}
	for (let p of this.points){
		strokeWeight(4);
		point(p.x, p.y);
	}
}
query(range,found){
	
	if(!this.boundary.intersects(range))
		return;
	for (let p of this.points){
		if(range.contains(p)){
			found.push(p);
		}
		count++;
	}
	if(this.divided){
		this.sonNO.query(range,found);
		this.sonNE.query(range,found);
		this.sonSO.query(range,found);
		this.sonSE.query(range,found);
	}

}
}
/*

function queryRange(range){
	// Prepare an array of results
	Array of XY pointsInRange;
	// Automatically abort if the range does not intersect this quad
	if (!boundary.intersectsAABB(range))
	return pointsInRange; // empty list
	// Check objects at this quad level
	for (int p = 0; p < points.size; p++)
	{
	if (range.containsPoint(points[p]))
	pointsInRange.append(points[p]);
	}
	// Terminate here, if there are no children
	if (northWest == null)
	return pointsInRange;
	// Otherwise, add the points from the children
	pointsInRange.appendArray(northWest->queryRange(range));
	pointsInRange.appendArray(northEast->queryRange(range));
	pointsInRange.appendArray(southWest->queryRange(range));
	pointsInRange.appendArray(southEast->queryRange(range));
	return pointsInRange;
}*/

