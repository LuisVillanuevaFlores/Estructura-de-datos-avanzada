var k = 2;

class Node{
	constructor(){
		this.point = null;
		this.left = null;
		this.right = null;
		this.visi = false;
	}
}
function getHeight(node) {
	if(node==null)return 0;
	return 1+ Math.max(getHeight(node.left),getHeight(node.right));
}
var line="";
function recorrer(node){
	if(node==null) return;
	if(node.left!=null){
		line+=(to_string(node)+"->"+to_string(node.left)+";");
	}
	if(node.right!=null){
		line+=(to_string(node)+"->"+to_string(node.right)+";");
	}
	recorrer(node.left);
	recorrer(node.right);
}
function to_string(node){
	var l="\"";
	for(var i=0;i<node.point.length;i++){
		
		if(i!=0){
			l+=",";
		}
		l+=(node.point[i]);
	}
	return l+"\"";
}
function generate_dot(node){
	line="digraph G{node [fontname=Arial,fontsize=\"15\",style=filled];";
	recorrer(node,line);
	line+="}";
	return line;
}
var size=0;
function build_kdtree(points, depth = 0){
	var n=points.length;
	size=Math.max(size,n);
	if(n==0) return null;
	var k=points[0].length;
	var axis=depth% k;
	//console.log(points);
	points.sort(function (a,b){
		//console.log("F",axis);
		//console.log(a[axis],b[axis]);
		//console.log(a[axis]- b[axis]);
		return a[axis]-b[axis];
	});
	var median=parseInt(n/2);
	var node=new Node();
	node.point=points[median];
	node.left=build_kdtree(points.slice(0,median),depth+1);
	node.right=build_kdtree(points.slice(median+1,n),depth+1);
	return node;
}
/*
function build_kdtree(points, depth = 0){
	var n=points.length;
	if(n==0) return null;
	
	if(n==1){
		
		return new Node(points[0],axis);
	}
	axis=depth% k;
	points.sort(compare);
	var node=new Node(points[parseInt(n/2)],axis);
	node.left=build_kdtree(points.slice(0,parseInt(n/2)),depth+1);
	node.right=build_kdtree(points.slice(parseInt(n/2)+1,n),depth+1);
	return node;
}
*/
function distanceSquared(point1, point2){
	//console.log(point1,point2);
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
	if(best==null||distanceSquared(best, point)> distanceSquared(node.point,point)){
		best=node.point;
	}
	if(node.point[axis]>point[axis]){
		return naive_closest_point(node.right, point, depth+1, best);
	}
	else{
		return naive_closest_point(node.left, point, depth+1, best);
	}
	
	
}

function naive_closest_point2(node, point, depth = 0, best = null){

	if(node==null)return best;

	var axis=depth%k;
	var next_best=null;
	var next_branch=null;
	if(best==null||distanceSquared(best, point)> distanceSquared(node.point,point))
		next_best=node.point;
	else
		next_best=best;
	if(point[axis]<node.point[axis])
		next_branch=node.left;
	else
		next_branch=node.right;
	return naive_closest_point2(next_branch,point,depth+1,next_best);
}

function closer_point(point,p1,p2){
	if(p1==null || p1.visi==true)
		return p2;
	if(p2==null || p2.visi==true)
		return p1;
	if(p1.visi==true && p2.visi==true)return ;
	if(distanceSquared(point,p1.point)<=distanceSquared(point,p2.point))
		return p1;	
	return p2;
}
function closest_point(node, point, depth = 0){
	if (node == null)
		return best;

	var axis = depth % k;
	var next_branch = null; //next node brach to look for
	var opposite_branch = null; //opposite
	if (point[axis] < node.point[axis]){
		next_branch = node.left;
		opposite_branch = node.right;
	}else{
		next_branch = node.right;
		opposite_branch = node.left;
	}
	
		
	var best=closer_point(point,closest_point(next_branch,point,depth+1),node);
	//console.log(best.point);
	if(distanceSquared(point,best.point)>Math.abs(point[axis]-node.point[axis]))
	{
		//best=closer_point(point,closest_point(opposite_branch,point,depth+1),node);
		best=closer_point(point,closer_point(point,closest_point(opposite_branch,point,depth+1),node),best);
	}

	return best;
}

function nearest(root,point,count){
	var list=[];
	for(var i=0;i<count;i++){
		var mejor=closest_point(root,point);
		mejor.visi=true;		
		list.push(mejor);

	}
return list;
	
}
function buscar(node, point,depth = 0,position, current, visitado, aux){
	if (node === null)
		return null;
	var value;
	if(visitado[position]){
		value=new Array(node.point.length).fill(Number.POSITIVE_INFINITY);
	}
	else{
		value=node.point;
	}
	var axis = depth % k;
	var next_branch = null; 
	var opposite_branch = null; 
	var PN=null,Po=null;

	if (point[axis] < node.point[axis]){
		PN=position*2;
		Po=position*2+1;
		next_branch = node.left;
		opposite_branch = node.right;
	}else{
		PN=position*2+1;
		Po=position*2;
		next_branch = node.right;
		opposite_branch = node.left;
	}

	var best=closer_point(point,buscar(next_branch,point,depth+1,PN,current,visitado,aux),value);
	if(best==node.point){
		current++;
		aux[position]=current;
	}

	if(distanceSquared(point,best)>Math.abs(point[axis]-node.point[axis])){
		//console.log(node.point,"A",position,Po);
		best=closer_point(point,buscar(opposite_branch,point,depth+1,Po,current,visitado,aux),value);
	}
	return best;
}
