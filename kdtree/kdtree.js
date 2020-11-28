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

	var median = Math.floor(points.length/2);

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

