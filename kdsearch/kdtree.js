var k = 2;

class Node{
	constructor(){
		this.point = null;
		this.left = null;
		this.right = null;
		this.visi = false;
	}
}

Array.prototype.unique=function(a){
  return function(){return this.filter(a)}}(function(a,b,c){return c.indexOf(a,b+1)<0
});

function distanceSquared(point1, point2){
	//console.log(point1,point2);
	var distance = 0;
	for (var i = 0; i < k; i++)
		distance += Math.pow((point1[i] - point2[i]), 2);
	return Math.sqrt(distance);
}

class Cola{
	constructor(cant){
		this.n=cant;
		this.lis=[];
	}
	agregar(distancia,x){
		for(var i=0;i<this.lis.length;i++){
			if(this.lis[i][1]==x)return;
		}
		if(this.lis.length==this.n){
			if(this.lis[this.n-1][0]>distancia){
        this.lis[this.n-1]=[distancia,x];
        this.lis.sort(function(a,b){
          return a[0]-b[0];
        });
      }
		}
    else{
      this.lis.push([distancia,x]);
      this.lis.sort(function(a,b){
        return a[0]-b[0];
      });
    }
    
	}

	agregar2(distancia,x,radio){
		for(var i=0;i<this.lis.length;i++){
			if(this.lis[i][1]==x)return;
		}
		if(distancia<radio){
			this.lis.push([distancia,x])
		}
	}
	agregar3(centro,x,l,a){
		for(var i=0;i<this.lis.length;i++){
			if(this.lis[i][1]==x)return;
		}
		//console.log(x)
		if((centro[0]+(l/2)>=x[0])&&(centro[0]-(l/2)<=x[0])){
			//console.log(x)
			if((centro[1]+(a/2)>=x[1])&&(centro[1]-(a/2)<=x[1])){
				this.lis.push([distanceSquared(centro,x),x])
				//console.log(x)
			}
		}
		this.lis.sort(function(a,b){
        	return a[0]-b[0];
      	});
	}
  mostrar(){
    console.log(this.lis)
  }
  top(){
  	return this.lis[this.lis.length-1][0];
  }
  llena(){
  	if(this.lis.length!=this.n)return false;
  	return true;
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
	if(p1==null && p2==null)return;
	if(p1==null)
		return p2;
	if(p2==null)
		return p1;
	
	if(distanceSquared(point,p1.point)<=distanceSquared(point,p2.point))
		return p1;	
	return p2;
}
function closest_point(node, point, depth = 0,cola){
	if (node == null)
		return;

	var axis = depth % k;
	var next_branch = null; //next node brach to look for
	var opposite_branch = null; //opposite
	cola.agregar(distanceSquared(point,node.point),node.point);
	if (point[axis] < node.point[axis]){
		next_branch = node.left;
		opposite_branch = node.right;
	}else{
		next_branch = node.right;
		opposite_branch = node.left;
	}
	
	
	//var best=closer_point(point,closest_point(next_branch,point,depth+1,cola),node);
	//cola.agregar(distanceSquared(point,best.point),best.point);
	closest_point(next_branch,point,depth+1,cola);
	if(!cola.llena() || cola.top()>Math.abs(point[axis]-node.point[axis]))
	{
		//best=closer_point(point,closest_point(opposite_branch,point,depth+1,cola),node);
		//best=closer_point(point,closer_point(point,closest_point(opposite_branch,point,depth+1,cola),node),best);
		//cola.agregar(distanceSquared(point,best.point),best.point);
		closest_point(opposite_branch,point,depth+1,cola)
	}
}

function nearest(root,point,count){
	var cola= new Cola(count);
	closest_point(root,point,0,cola)
	//cola.agregar(0,[5,2])
	return cola.lis;
	
}


function range_query_circle(node,center,radio,cola,depth=0){
	if (node == null)
		return;

	var axis = depth % k;
	var next_branch = null; //next node brach to look for
	var opposite_branch = null; //opposite
	cola.agregar2(distanceSquared(center,node.point),node.point,radio);
	if (point[axis] < node.point[axis]){
		next_branch = node.left;
		opposite_branch = node.right;
	}else{
		next_branch = node.right;
		opposite_branch = node.left;
	}
	
	
	//var best=closer_point(point,closest_point(next_branch,point,depth+1,cola),node);
	//cola.agregar(distanceSquared(point,best.point),best.point);
	range_query_circle(next_branch,center,radio,cola,depth+1);
	if(!cola.llena() || cola.top()>Math.abs(point[axis]-node.point[axis]))
	{
		//best=closer_point(point,closest_point(opposite_branch,point,depth+1,cola),node);
		//best=closer_point(point,closer_point(point,closest_point(opposite_branch,point,depth+1,cola),node),best);
		//cola.agregar(distanceSquared(point,best.point),best.point);
		range_query_circle(opposite_branch,center,radio,cola,depth+1)
	}
}

function nearest2(root,center,radio){
	var cola= new Cola(5);
	range_query_circle(root,center,radio,cola)
	return cola.lis;
	
}

function range_query(node,center,l,a,cola,depth=0){
	if (node == null)
		return;

	var axis = depth % k;
	var next_branch = null; //next node brach to look for
	var opposite_branch = null; //opposite
	cola.agregar3(center,node.point,l,a);
	if (point[axis] < node.point[axis]){
		next_branch = node.left;
		opposite_branch = node.right;
	}else{
		next_branch = node.right;
		opposite_branch = node.left;
	}
	
	
	//var best=closer_point(point,closest_point(next_branch,point,depth+1,cola),node);
	//cola.agregar(distanceSquared(point,best.point),best.point);
	range_query(next_branch,center,l,a,cola,depth+1);
	if(!cola.llena() || cola.top()>Math.abs(point[axis]-node.point[axis]))
	{
		//best=closer_point(point,closest_point(opposite_branch,point,depth+1,cola),node);
		//best=closer_point(point,closer_point(point,closest_point(opposite_branch,point,depth+1,cola),node),best);
		//cola.agregar(distanceSquared(point,best.point),best.point);
		range_query(opposite_branch,center,l,a,cola,depth+1)
	}
}

function nearest3(root,center,l,a){
	var cola= new Cola(1000);
	range_query(root,center,l,a,cola)
	return cola.lis;
	
}
