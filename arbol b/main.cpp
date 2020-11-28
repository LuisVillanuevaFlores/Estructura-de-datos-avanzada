#include "B+.h"

int main(){

    BPTree arbol;
    FILE* f;
    int op;
    string s,codigo,sucursal,saldo;
    cout<<"Desea recuperar un arbol ?"<<endl;
    cout << "[0] SI" << endl;
    cout << "[1] NO" << endl;
    cin>>op;
    if(op==0){
        //arbol.recuperar();
        //MODIFICAS EL MAX ese es el orden
    }
    else{
        cout<<"Ingrese orden del arbol"<<endl;
        cin>>op;
        MAX=op-1;
    }
    system("pause");
    do {
        system("cls");
        cout << "Menu principal" << endl;
        cout << "========================" << endl;
        cout << "[1] Agregar registro" << endl;
        cout << "[2] Mostrar registros" << endl;
        cout << "[3] Eliminar registro" << endl;
        cout << "[4] Buscar registro" << endl;
        cout << "[5] Ingresar DATA" << endl;
        cout << "[0] Salir" << endl;
        cout << "========================" << endl;
        cout << "Ingresa la opcion: ";
        cin>>op;
        cin.ignore();
        switch (op){
        case 1:{
            cout<<"Ingrese codigo: ";
            cin>>codigo;
            f=fopen("a.txt","rb+");
            fseek(f,0,2);
            int pos=ftell(f);
            cout<<"Ingrese sucursal: ";
            cin>>sucursal;
            cout<<"Ingrese saldo: ";
            cin>>saldo;
            fprintf(f,"%10s %18s %12s\n",codigo.c_str(),sucursal.c_str(),saldo.c_str());
            fclose(f);
            arbol.insert(codigo,pos);
            system("pause");
            break;
        }
        case 2:
            arbol.display(arbol.getRoot());
            arbol.graficar();
            system("pause");
            break;
        case 3:{
            cout<<"Ingrese codigo: ";
            cin>>codigo;
            f=fopen("a.txt","rb+");
            int aux=arbol.remove(codigo);
            if(aux!=-1){
                fpos_t pos=aux;
                fsetpos(f,&pos);
                fprintf(f,"%43s","\n");
            }
            fclose(f);
            system("pause");
            break;}
        case 4:{
            cout<<"Ingrese codigo: ";
            cin>>s;
            ifstream infile;
            infile.open("a.txt");
            char cod[10],suc[18],sal[12];
            int pos=arbol.search(s);
            if(pos!=-1){
                infile.seekg(pos,infile.beg);
                cout<<pos<<endl;
                infile>>cod>>suc>>sal;
                cout<<"Codigo: "<<cod<<endl;
                cout<<"Sucursal: "<<suc<<endl;
                cout<<"Saldo: "<<sal<<endl;
            }
            infile.close();
            system("pause");
            break;}
        case 5:
            arbol.leer();
            system("pause");
            break;
        case 0:
            return 0;
        default:
            printf("Opcion incorrecta\n");
            system("pause");
            break;

        }
    }while(op!=0);


    return 0;
}
