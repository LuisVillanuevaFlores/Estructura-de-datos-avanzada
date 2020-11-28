k = 2;
class Node{
	constructor(point, axis){
		this.point = point;
		this.left = null;
		this.right = null;
		this.axis = axis;
	}
}


function build_kdtree(points, depth = 0){
	if(points.length==0)return null;

	var axis = depth % k;
	//console.log(points.length);
	points.sort(function (a,b){
		return a[axis]>b[axis];
	});

	var median = int(points.length/2);

	var node = new Node(points[median],axis);
	node.left=build_kdtree(points.slice(0,median),depth+1);
	node.right=build_kdtree(points.slice(median+1,points.length),depth+1);

	return node;
	
}

function getHeight(node) {
	if(node == null)   
	{
		return 0;
	}
	else   
	{
		return 1 +(Math.max(getHeight(node.left),getHeight(node.right)));   
	}
}




function generate_dot(node){
	var cad="";

	if(node==null)
		return "";
	
	if(node.left!=null){
		cad=cad+'"'+node.point.toString()+"\"";

		cad=cad+" -> "+'"'+node.left.point.toString()+'"'+";"+"\n";
	}
	if(node.right!=null){
		cad=cad+"\""+node.point.toString()+"\"";
		cad=cad+" -> "+'"'+node.right.point.toString()+'"'+";"+"\n";
	}
	return cad+generate_dot(node.left)+generate_dot(node.right);
}

function distanceSquared(point1, point2){
	var distance = 0;
	for (var i = 0; i < k; i++)
		distance += Math.pow((point1[i] - point2[i]), 2);
	return Math.sqrt(distance);
}

function closest_point_brute_force(points, point){
	var m=distanceSquared(points[0],point);
	var pointm=points[0];
	for (var i = 1; i < points.length; i++) {
		var aux=distanceSquared(points[i],point);
		if(aux<m){
			m=aux;
			pointm=points[i];
		}
	}
	return pointm;



}

function naive_closest_point(node, point, depth = 0, best = null){

	if(node==null)return best;

	var axis=depth% k;
	if(best==null){
		best=node.point;
	}
	else if((distanceSquared(best, point)> distanceSquared(node.point,point))){
		best=node.point;
	}
	console.log(axis)
	if(axis==0){
		if(point[0]>node.point[0]){
			node=node.right
		}
		else
			node=node.left
		console.log(node)
	}
	else{
		if(point[1]>node.point[1])
			node=node.right
		else
			node=node.left
		console.log(node)
	}
	return naive_closest_point(node,point,depth+1,best)	
}

function closer_point(point, p1, p2){
	if(p1==null)
		return p2;
	if(p2==null)
		return p1;
	if(distanceSquared(point,p1)<distanceSquared(point,p2))
		return p1;
	else return p2;
}