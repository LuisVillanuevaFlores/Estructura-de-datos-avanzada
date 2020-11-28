#include <bits/stdc++.h>
using namespace std;

int main(){
    int tra,aux=0,sum=0;
    cin>>tra;
    vector<int> pepito;
    vector<int> orde;
    vector<pair<int,int> > orde2;
    vector<int> res;
    res.resize(tra);
    bool sw=true,sw2=true,entro=false;
    for(int i=0;i<tra;i++){
        int lle;int ser;
        cout<<"Hora de llegada: ";cin>>lle;
        cout<<"Tiempo de servicio: ";cin>>ser;
        entro=false;
        if(sw){
            if(sw2){
                sum=lle;
                sw2=false;
                orde.push_back(lle);
                orde2.push_back(make_pair(ser,i));
            }
            //sum=lle;
            else{
                if(lle==sum){
                    orde.push_back(lle);
                    orde2.push_back(make_pair(ser,i));
                    entro=true;
                    if(i==tra-1)sw=false;
                }
                else{
                    sort(orde2.begin(), orde2.end());
                    sum=sum+orde2[0].first;
                    res[orde2[0].second]=sum;
                    
                    //orde2.clear();
                    orde2.erase(orde2.begin());                    
                    sw=false;
                    ////////
                }
            }
            //sw=false;
        }
        if(sw==false){
        	if(sum>=lle && entro==false){
                orde.push_back(lle);
                orde2.push_back(make_pair(ser,i));
            }
            if(sum<lle || i==tra-1){
                sort(orde2.begin(), orde2.end());
                for(int j=0;j<orde2.size();j++){
                    sum=sum+orde2[j].first;
                    res[orde2[j].second]=sum;
                }
                orde2.clear();
                orde2.push_back(make_pair(ser,i));
                orde.push_back(lle);
                if(lle>sum && i==tra-1){
                    res[tra-1]=lle+ser;                    
                }
                if(lle>sum && i!=tra-1){
                    sw=true;
                    sum=lle;
                }
            }
        }
    }
    for(int i=0;i<res.size();i++){
        cout<<res[i]<<endl;
    }
    cout<<"---------------------------"<<endl;
     for(int i=0;i<res.size();i++){
        cout<<res[i]-orde[i]<<endl;
    }
}
