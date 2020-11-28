#include<bits/stdc++.h>
using namespace std;

class point
{
public:
	int x,y;
	point(int a,int b){
		x=a;
		y=b;
	}
};

class mbr
{
public:
	int maxi;
	int perimeter;
	
	int largo;
	int ancho;
	mbr( int m){
		
		maxi=m;
	}

	int getperim(){
		return perimeter;
	}

	void calperim(point izinf,point dersup){
		largo=abs(izinf.y-dersup.y);
		ancho=abs(izinf.x-dersup.x);

		perimeter= largo*ancho*2;
	}

	void updateper(vector<point> b){
		int c=calperim(b[0],b[1]);	
		for(int i=0;i<b.size();i++){
			for(int j=0;j<b.size();j++){
				if(c==0)continue;
				else if(calperim(b[i],b[j])<c){
					c=calperim(b[i],b[j]);
				}

			}

		}
		perimeter=c;


	}
};

class nodo
{
	
public:
	vector<point>datos;
	vector<mbr>nodes;
	bool isleaf;
	nodo(){
		isleaf=true;
	}
	
};

bool sortPx(point a1, point a2) {
	return a1.x < a2.x; 
}
bool sortPy(point a1, point a2) {
	return a1.y < a2.y; 
}

class rtree
{
	
public:
	mbr M;
	int max;
	nodo* root;
	rtree(int num){
		max=num;
		root=new nodo();
	}

	mbr choose_subtree(nodo *u,point p){
		mbr c(this->max);
		for(int i=0;i<u->nodes.size();i++){
			if(u->nodes[i]->calperim(u->datos[i],p)<u->nodes[i+1]->calperim(u->datos[i+1],p)){
				c=u->nodes[i];
			}

		}
		return c;		


	}
	void insert(nodo *u, point p){
		if(u->isleaf){
			u->datos.push_back(p);
			if(this.max<u->datos.size()){
				handle_overflow(u);
			}
		}
		
		else{
			nodo *v=new nodo();
			v=choose_subtree(u,p);
			insert(v,p);
		}
	
	}
	void handle_overflow(nodo *u){
		if(u->isleaf)
			splitL(u);
		else
			split(u);
		if(this->root==u){
			nodo* aux=new nodo();
			aux=u;
			aux->isleaf=false;
			root->nodes=u;

		}
		else{
			nodo* aux=new nodo();
			aux->nodes=u;
			updateper(aux->nodes);
			if(this->max<aux->nodes.size()){
				handle_overflow(aux);
			}
			
		}
	}



	void splitL(nodo *u){
		vector<nodo>a;
		vector<nodo>b;
		int m=u->datos.size();
		sort(u->datos.begin(),u->datos.end(),sortPx);
		for (int i =ceil(0.4*this->max) ; i < m-ceil(0.4*this->max); ++i)
		{	
			a.datos.push_back(u->datos[i]);
		}

		for(int i=0;i<this->u->datos.size();i++){
			for(int j=0;j<a.size();j++){
				if(a.datos[i]!=u->datos[i]){
					b.datos.push_back(u->datos[i]);
				}
			}
		}
	}

	void split(nodo *u){
		vector<nodo>a;
		vector<nodo>b;
		int m=u->datos.size();
		sort(u->datos.begin(),u->datos.end(),sortPx);
		for (int i =ceil(0.4*this->max) ; i < m-ceil(0.4*this->max); ++i)
		{	
			a.nodes.push_back(u->nodes[i]);
		}

		for(int i=0;i<this->u->datos.size();i++){
			for(int j=0;j<a.size();j++){
				if(a.nodes[i]!=u->nodes[i]){
					b.nodes.push_back(u->nodes[i]);
				}
			}
		}
	}
	
};









