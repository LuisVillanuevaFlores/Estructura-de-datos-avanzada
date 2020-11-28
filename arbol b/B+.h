#include<bits/stdc++.h>
using namespace std;

struct indice{
    string key;
    int pos;
    indice(string c="&",int p=0):key(c),pos(p){};

    indice& operator = (const indice &p){
        this->key=p.key;
        this->pos=p.pos;
        return *this;
    }
    bool operator <(const string a)const{return this->key<a;}
    bool operator >(const string a)const{return this->key>a;}
    bool operator <(const indice a)const{return this->key<a.key;}
    bool operator >(const indice a)const{return this->key>a.key;}
    bool operator == (const indice &p) const{
        return this->key == p.key && this->pos == p.pos;
    }
};
bool operator <(string a,indice b){
        return a<b.key;
}
bool operator >(string a,indice b){
        return a>b.key;
}
int MAX;
class BPTree;
class Node{
	bool IS_LEAF;
	indice *key;
	int size;
	Node** ptr;
	friend class BPTree;
public:
	Node();
};
class BPTree{
	Node *root;
	void insertInternal(indice,Node*,Node*);
	void removeInternal(indice,Node*,Node*);
	Node* findParent(Node*,Node*);
public:
	BPTree();
	int search(string);
	void insert(string,int);
	int remove(string);
	void graficar();
	int recorrer(Node *p,ofstream&in,int&con);
	void display(Node*);
	void leer();
	Node* getRoot();
	void cleanUp(Node*);
	~BPTree();
};
Node::Node(){
	key = new indice[MAX];
	ptr = new Node*[MAX+1];
}
BPTree::BPTree(){
	root = nullptr;
}
int BPTree::search(string x){
	if(root==nullptr){
		cout<<"Arbol vacio\n";
	}
	else{
		Node* cursor = root;
		while(cursor->IS_LEAF==false){
			for(int i = 0; i < cursor->size; i++){
				if(x < cursor->key[i].key){
					cursor = cursor->ptr[i];
					break;
				}
				if(i == cursor->size - 1){
					cursor = cursor->ptr[i+1];
					break;
				}
			}
		}
		for(int i = 0; i < cursor->size; i++){
			if(cursor->key[i].key == x){
				cout<<"Encontrado\n";
				return cursor->key[i].pos;
			}
		}
		return -1;
		cout<<"No encontrado\n";
	}
}
void BPTree::insert(string x,int pos){
    indice in(x,pos);
	if(root==nullptr){
        cout<<"A"<<x<<endl;
		root = new Node;
		root->key[0] = in;
		root->IS_LEAF = true;
		root->size = 1;
		cout<<"Raiz creada\n"<<x<<": Insertado correctamente\n";
	}
	else{
		Node* cursor = root;
		Node* parent;
		while(cursor->IS_LEAF == false){
			parent = cursor;
			for(int i = 0; i < cursor->size; i++){
				if(x<cursor->key[i]){
					cursor = cursor->ptr[i];
					break;
				}
				if(i == cursor->size - 1){
					cursor = cursor->ptr[i+1];
					break;
				}
			}
		}
		if(cursor->size < MAX){
			int i = 0;
			while(x > cursor->key[i] && i < cursor->size) i++;
			for(int j = cursor->size;j > i; j--){
				cursor->key[j] = cursor->key[j-1];
			}
			cursor->key[i] = in;
			cursor->size++;
			cursor->ptr[cursor->size] = cursor->ptr[cursor->size-1];
			cursor->ptr[cursor->size-1] = nullptr;
			cout<<x<<": Insertado correctamente\n";
		}
		else{
			cout<<x<<": Insertado correctamente\n";
			cout<<"Nodo hoja lleno!\n Separando nodo hoja\n";

			Node* newLeaf = new Node;
			indice virtualNode[MAX+1];
			for(int i = 0; i < MAX; i++){
				virtualNode[i] = cursor->key[i];
			}
			int i = 0, j;
			while(x > virtualNode[i] && i < MAX) i++;
			for(int j = MAX;j > i; j--){
				virtualNode[j] = virtualNode[j-1];
			}
			virtualNode[i] = in;
			newLeaf->IS_LEAF = true;
			cursor->size = (MAX+1)/2;
			newLeaf->size = MAX+1-(MAX+1)/2;
			cursor->ptr[cursor->size] = newLeaf;
			newLeaf->ptr[newLeaf->size] = cursor->ptr[MAX];
			cursor->ptr[MAX] = nullptr;
			for(i = 0; i < cursor->size; i++){
				cursor->key[i] = virtualNode[i];
			}
			for(i = 0, j = cursor->size; i < newLeaf->size; i++, j++){
				newLeaf->key[i] = virtualNode[j];
			}
			if(cursor == root){
				Node* newRoot = new Node;
				newRoot->key[0] = newLeaf->key[0];
				newRoot->ptr[0] = cursor;
				newRoot->ptr[1] = newLeaf;
				newRoot->IS_LEAF = false;
				newRoot->size = 1;
				root = newRoot;
				cout<<"Nueva raiz creada\n";
			}
			else{
				insertInternal(newLeaf->key[0],parent,newLeaf);
			}
		}
	}
}
void BPTree::insertInternal(indice x, Node* cursor, Node* child){
	cout<<"Insertando nodo interno: "<<x.key<<endl;
	if(cursor->size < MAX){
		int i = 0;
		while(x > cursor->key[i] && i < cursor->size) i++;
		for(int j = cursor->size;j > i; j--){
			cursor->key[j] = cursor->key[j-1];
		}
		for(int j = cursor->size+1; j > i+1; j--){
			cursor->ptr[j] = cursor->ptr[j-1];
		}
		cursor->key[i] = x;
		cursor->size++;
		cursor->ptr[i+1] = child;
		cout<<"Nodo interior insertado correctamente\n";
	}
	else{
	    cout<<"Nodo interior insertado correctamente\n";
        cout<<"Nodo interior lleno\n Dividiendo nodo interno\n";
		Node* newInternal = new Node;
		indice virtualKey[MAX+2];
		Node* virtualPtr[MAX+2];
		for(int i = 0; i < MAX; i++){
			virtualKey[i] = cursor->key[i];
		}
		for(int i = 0; i < MAX+1; i++){
			virtualPtr[i] = cursor->ptr[i];
		}
		int i = 0, j;
		while(x > virtualKey[i] && i < MAX) i++;
		//ERROR
		for(int j = MAX+1;j > i; j--){
			virtualKey[j] = virtualKey[j-1];
		}
		virtualKey[i] = x;
		for(int j = MAX+2;j > i+1; j--){
			virtualPtr[j] = virtualPtr[j-1];
		}
		virtualPtr[i+1] = child;
		newInternal->IS_LEAF = false;
		cursor->size = (MAX+1)/2;
		newInternal->size = MAX-(MAX+1)/2;
		for(i = 0, j = cursor->size+1; i < newInternal->size; i++, j++){
			newInternal->key[i] = virtualKey[j];
		}
		for(i = 0, j = cursor->size+1; i < newInternal->size+1; i++, j++){
			newInternal->ptr[i] = virtualPtr[j];
		}
		if(cursor == root){
			Node* newRoot = new Node;
			newRoot->key[0] = cursor->key[cursor->size];
			newRoot->ptr[0] = cursor;
			newRoot->ptr[1] = newInternal;
			newRoot->IS_LEAF = false;
			newRoot->size = 1;
			root = newRoot;
			cout<<"Creando nueva raiz\n";
		}
		else{
			insertInternal(cursor->key[cursor->size] ,findParent(root,cursor) ,newInternal);
		}
	}
}
Node* BPTree::findParent(Node* cursor, Node* child){
	Node* parent;
	if(cursor->IS_LEAF || (cursor->ptr[0])->IS_LEAF){
		return nullptr;
	}
	for(int i = 0; i < cursor->size+1; i++){
		if(cursor->ptr[i] == child){
			parent = cursor;
			return parent;
		}
		else{
			parent = findParent(cursor->ptr[i],child);
		}
	}
	return parent;
}
int BPTree::remove(string x){
	if(root==nullptr){
		cout<<"ARbol vacio\n";
	}
	else{
        int aux=-1;
		Node* cursor = root;
		Node* parent;
		int leftSibling, rightSibling;
		while(cursor->IS_LEAF == false){
			for(int i = 0; i < cursor->size; i++){
				parent = cursor;
				leftSibling = i-1;
				rightSibling =  i+1;
				if(x < cursor->key[i]){
					cursor = cursor->ptr[i];
					break;
				}
				if(i == cursor->size - 1){
					leftSibling = i;
					rightSibling = i+2;
					cursor = cursor->ptr[i+1];
					break;
				}
			}
		}
		bool found = false;
		int pos;
		if(cursor==nullptr){
            cout<<"NULO\n";
        }
		for(pos = 0; pos < cursor->size; pos++){
			cout<<"pos"<<pos<<endl;
			if(cursor->key[pos].key == x){
				found = true;
                aux=cursor->key[pos].pos;
				break;
			}
		}
		if(!found){
			cout<<"No encontrado\n";
			return -1;
		}
		cout<<pos<<endl;
		cout<<cursor->key[pos].key<<endl;
		cout<<cursor->size<<endl;
		cout<<"A"<<endl;
		for(int i = pos; i < cursor->size-1; i++){
            cout<<"i"<<i<<endl;
			cursor->key[i] = cursor->key[i+1];
		}
		cursor->size--;
        cout<<"FIN2"<<endl;
		if(cursor == root){
			cout<<x<<"Eliminado de un nodo hoja 1\n";

			for(int i = 0; i < MAX+1; i++){
				cursor->ptr[i] = nullptr;
			}
			if(cursor->size == 0){
				cout<<"Arbol eliminado\n";
				delete[] cursor->key;
				delete[] cursor->ptr;
				delete cursor;
				root = nullptr;
			}
			return aux;
		}
		cursor->ptr[cursor->size] = cursor->ptr[cursor->size+1];
		cursor->ptr[cursor->size+1] = nullptr;
		cout<<x<<"Eliminado de un nodo hoja 2\n";
		if(cursor->size >= (MAX+1)/2){

			return aux;
		}
		cout<<"Desbordamiento en nodo hoja!\n";
		if(leftSibling >= 0){
			Node *leftNode = parent->ptr[leftSibling];
			if(leftNode->size >= (MAX+1)/2+1){
				for(int i = cursor->size; i > 0; i--){
					cursor->key[i] = cursor->key[i-1];
				}
				cursor->size++;
				cursor->ptr[cursor->size] = cursor->ptr[cursor->size-1];
				cursor->ptr[cursor->size-1] = nullptr;
				cursor->key[0] = leftNode->key[leftNode->size-1];
				leftNode->size--;
				leftNode->ptr[leftNode->size] = cursor;
				leftNode->ptr[leftNode->size+1] = nullptr;
				parent->key[leftSibling] = cursor->key[0];
				cout<<cursor->key[0].key<<" transferido de hermano izquierdo del nodo hoja\n";
				return aux;
			}
		}
		if(rightSibling <= parent->size){
			Node *rightNode = parent->ptr[rightSibling];
			if(rightNode->size >= (MAX+1)/2+1){
				cursor->size++;
				cursor->ptr[cursor->size] = cursor->ptr[cursor->size-1];
				cursor->ptr[cursor->size-1] = nullptr;
				cursor->key[cursor->size-1] = rightNode->key[0];
				rightNode->size--;
				rightNode->ptr[rightNode->size] = rightNode->ptr[rightNode->size+1];
				rightNode->ptr[rightNode->size+1] = nullptr;
				for(int i = 0; i < rightNode->size; i++){
					rightNode->key[i] = rightNode->key[i+1];
				}
				parent->key[rightSibling-1] = rightNode->key[0];
				cout<<cursor->key[cursor->size-1].key<<" transferido de hermano izquierdo del nodo hoja\n";
				return aux;
			}
		}
		if(leftSibling >= 0){
			Node* leftNode = parent->ptr[leftSibling];
			for(int i = leftNode->size, j = 0; j < cursor->size; i++, j++){
				leftNode->key[i] = cursor->key[j];
			}
			leftNode->ptr[leftNode->size] = nullptr;
			leftNode->size += cursor->size;
			leftNode->ptr[leftNode->size] = cursor->ptr[cursor->size];
			cout<<"Uniendo dos nodos hojas\n";
			removeInternal(parent->key[leftSibling],parent,cursor);
			cout<<"A"<<endl;
			delete[] cursor->key;
			delete[] cursor->ptr;
			delete cursor;
			cout<<"B"<<endl;
		}
		else if(rightSibling <= parent->size){
			Node* rightNode = parent->ptr[rightSibling];
			for(int i = cursor->size, j = 0; j < rightNode->size; i++, j++){
				cursor->key[i] = rightNode->key[j];
			}
			cursor->ptr[cursor->size] = nullptr;
			cursor->size += rightNode->size;
			cursor->ptr[cursor->size] = rightNode->ptr[rightNode->size];
			cout<<"Uniendo dos nodos hojas\n";
			removeInternal(parent->key[leftSibling+1],parent,rightNode);
			delete[] rightNode->key;
			delete[] rightNode->ptr;
			delete rightNode;
		}
		return aux;
	}

}
void BPTree::removeInternal(indice x, Node* cursor, Node* child){
	if(cursor == root){
		if(cursor->size == 1){
			if(cursor->ptr[1] == child){
				delete[] child->key;
				delete[] child->ptr;
				delete child;
				root = cursor->ptr[0];
				delete[] cursor->key;
				delete[] cursor->ptr;
				delete cursor;
				cout<<"Nodo raiz cambiado 1\n";
				return;
			}
			else if(cursor->ptr[0] == child){
				delete[] child->key;
				delete[] child->ptr;
				delete child;
				root = cursor->ptr[1];
				delete[] cursor->key;
				delete[] cursor->ptr;
				delete cursor;
				cout<<"Nodo raiz cambiado 2\n";
				return;
			}
		}
	}
	int pos;
	for(pos = 0; pos < cursor->size; pos++){
		if(cursor->key[pos] == x){
			break;
		}
	}
	for(int i = pos; i < cursor->size; i++){
		cursor->key[i] = cursor->key[i+1];
	}
	for(pos = 0; pos < cursor->size+1; pos++){
		if(cursor->ptr[pos] == child){
			break;
		}
	}
	for(int i = pos; i < cursor->size+1; i++){
		cursor->ptr[i] = cursor->ptr[i+1];
	}
	cursor->size--;
	if(cursor->size >= (MAX+1)/2-1){
        cout<<x.key<<" Eliminado de nodo interno\n";
		return;
	}
	cout<<"Desbordamiento en nodo interno!\n";
	Node* parent = findParent(root, cursor);
	int leftSibling, rightSibling;
	for(pos = 0; pos < parent->size+1; pos++){
		if(parent->ptr[pos] == cursor){
			leftSibling = pos - 1;
			rightSibling = pos + 1;
			break;
		}
	}
	if(leftSibling >= 0){
		Node *leftNode = parent->ptr[leftSibling];
		if(leftNode->size >= (MAX+1)/2){
			for(int i = cursor->size; i > 0; i--){
				cursor->key[i] = cursor->key[i-1];
			}
			cursor->key[0] = parent->key[leftSibling];
			parent->key[leftSibling] = leftNode->key[leftNode->size-1];
			for (int i = cursor->size+1; i > 0; i--){
				cursor->ptr[i] = cursor->ptr[i-1];
			}
			cursor->ptr[0] = leftNode->ptr[leftNode->size];
			cursor->size++;
			leftNode->size--;
            cout<<cursor->key[0].key<<" Transferido de hermano izquierdo de nodo interno\n";
			return;
		}
	}
	if(rightSibling <= parent->size){
		Node *rightNode = parent->ptr[rightSibling];
		if(rightNode->size >= (MAX+1)/2){
			cursor->key[cursor->size] = parent->key[pos];
			parent->key[pos] = rightNode->key[0];
			for (int i = 0; i < rightNode->size -1; i++){
				rightNode->key[i] = rightNode->key[i+1];
			}
			cursor->ptr[cursor->size+1] = rightNode->ptr[0];
			for (int i = 0; i < rightNode->size; ++i){
				rightNode->ptr[i] = rightNode->ptr[i+1];
			}
			cursor->size++;
			rightNode->size--;
            cout<<cursor->key[0].key<<" Transferido de hermano derecho de nodo interno\n";
			return;
		}
	}
	if(leftSibling >= 0){
		Node *leftNode = parent->ptr[leftSibling];
		leftNode->key[leftNode->size] = parent->key[leftSibling];
		for(int i = leftNode->size+1, j = 0; j < cursor->size; j++){
			leftNode->key[i] = cursor->key[j];
		}
		for(int i = leftNode->size+1, j = 0; j < cursor->size; j++){
			leftNode->ptr[i] = cursor->ptr[j];
			cursor->ptr[j] = nullptr;
		}
		leftNode->size += cursor->size+1;
		cursor->size = 0;
		removeInternal(parent->key[leftSibling], parent, cursor);
		cout<<"Mezclando con hermano izquierdo\n";
	}
	else if(rightSibling <= parent->size){
		Node *rightNode = parent->ptr[rightSibling];
		cursor->key[cursor->size] = parent->key[leftSibling];
		for(int i = cursor->size+1, j = 0; j < rightNode->size; j++){
			cursor->key[i] = rightNode->key[j];
		}
		for(int i = cursor->size+1, j = 0; j < rightNode->size; j++){
			cursor->ptr[i] = rightNode->ptr[j];
			rightNode->ptr[j] = nullptr;
		}
		cursor->size += rightNode->size+1;
		rightNode->size = 0;
		removeInternal(parent->key[leftSibling], parent, rightNode);
		cout<<"Mezclando con hermano derecho\n";
	}
}
void BPTree::display(Node* cursor){
	if(cursor!=nullptr){
		for(int i = 0; i < cursor->size; i++){
			cout<<cursor->key[i].key<<":"<<cursor->key[i].pos<<" ";
		}
		cout<<"\n";
		if(cursor->IS_LEAF != true){
			for(int i = 0; i < cursor->size+1; i++){
				display(cursor->ptr[i]);
			}
		}
	}
}
Node* BPTree::getRoot(){
	return root;
}
void BPTree::cleanUp(Node* cursor){
	if(cursor!=nullptr){
		if(cursor->IS_LEAF != true){
			for(int i = 0; i < cursor->size+1; i++){
				cleanUp(cursor->ptr[i]);
			}
		}
		for(int i = 0; i < cursor->size; i++){
		    cout<<cursor->key[i].key<<" eliminado de memoria\n";
		}
        cout<<"I"<<endl;
		delete[] cursor->key;
		cout<<"A"<<endl;
		delete[] cursor->ptr;
		cout<<"B"<<endl;
		delete cursor;
		cout<<"C"<<endl;
	}
}
BPTree::~BPTree(){
	cleanUp(root);
}

void BPTree::leer(){
    FILE*f;
    f=fopen("a.txt","rb+");
    ifstream infile;
    infile.open("Entrada.txt");
    char cod[10],suc[18],sal[12];
    int pos;
    while(!infile.eof()){
        fseek(f,0,2);
        int pos=ftell(f);
        infile>>cod>>suc>>sal;
        string aux(cod);
        this->insert(aux,pos);
        fprintf(f,"%10s %18s %12s\n",cod,suc,sal);
    }
    fclose(f);
    infile.close();

}
int BPTree::recorrer(Node *cursor,ofstream&in,int&con){
    if(cursor==nullptr)return -1;
    int aux=con;
    in<<con++<<"[label=\"";
    in<<"<f0> |";
    int j=0;
    for(int i = 1; i < cursor->size*2+1; i++){
        in<<"<f"<<to_string(i)<<">";
        in<<cursor->key[j++].key;
        in<<"|";
        i++;
        in<<"<f"<<to_string(i)<<">";
        if(i!=cursor->size*2)in<<"|";
    }
    in<<"\"]\n";
    if(cursor->IS_LEAF)return aux;
    for(int i = 0; i < cursor->size+1; i++){
        in<<aux<<":f"<<i*2<<"->"<<recorrer(cursor->ptr[i],in,con)<<":f0"<<endl;
    }
    return aux;


}
void BPTree::graficar(){
    int con=0;
    ofstream in("b.txt");
    in<<"digraph G{\n";
    in<<"node [shape=record];\n";
    recorrer(this->root,in,con);
    in<<"}";
    in.close();
    string out="dot -Tpng b.txt -o a.png";
    char*a=&out[0];
    system(a);
    out="start a.png";
    a=&out[0];
    system(a);

}
