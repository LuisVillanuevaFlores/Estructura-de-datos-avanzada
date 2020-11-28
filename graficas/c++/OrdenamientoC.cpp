#include <bits/stdc++.h>
using namespace std;

void CountSort(vector<int>& arr){
    int maximo = *max_element(arr.begin(), arr.end());
    int minimo = *min_element(arr.begin(), arr.end());
    int rango = maximo - minimo + 1;
    vector<int> count(rango), output(arr.size());
    for(int i = 0; i < arr.size(); i++)
        count[arr[i]-minimo]++;
    for(int i = 1; i < count.size(); i++)
           count[i] += count[i-1];
    for(int i = arr.size()-1; i >= 0; i--){
         output[ count[arr[i]-minimo] -1 ] = arr[i];
              count[arr[i]-minimo]--;
    }

    for(int i=0; i < arr.size(); i++)
            arr[i] = output[i];
}
void merges(vector<int>& arr, int l, int m, int r){
    int i, j, k;
    int n1 = m - l + 1;
    int n2 =  r - m;
    int L[n1], R[n2];
    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1+ j];
    i = j= 0;
    k = l;
    while (i < n1 && j < n2){
        if (L[i] <= R[j]){
            arr[k] = L[i];
            i++;
        }
        else{
            arr[k] = R[j];
            j++;
        }
        k++;
    }
    while (i < n1){
        arr[k] = L[i];
        i++;
        k++;
    }
    while (j < n2){
        arr[k] = R[j];
        j++;
        k++;
    }
}
void mergeSort(vector<int>& arr, int l, int r){
    if (l < r){
        int m = l+(r-l)/2;
        mergeSort(arr, l, m);
        mergeSort(arr, m+1, r);
        merges(arr, l, m, r);
    }
}
void MergeSort(vector<int>& arr){
    mergeSort(arr,0,arr.size());
}
void BubbleSort(vector<int>& arr) {
    int n=arr.size();
  int x,y,tmp;
  for(x = 1; x < n; x++) {
    for(y = 0; y < n - x; y++) {
      if(arr[y] > arr[y + 1]) {
        tmp = arr[y];
        arr[y] = arr[y + 1];
        arr[y + 1] = tmp;
      }
    }
  }
}
void SelectionSort(vector<int> &arr) {
    int n=arr.size();
  int x, y, min, tmp;
  for(x = 0; x < n; x++) {
    min = x;
    for(y = x + 1; y < n; y++) {
      if(arr[min] > arr[y]) {
        min = y;
      }
    }
    tmp = arr[min];
    arr[min] = arr[x];
    arr[x] = tmp;
  }
}
void heapify(vector<int> &arr, int n, int i){
    int largest = i;
    int l = 2*i + 1;
    int r = 2*i + 2;
    if (l < n && arr[l] > arr[largest])
        largest = l;
    if (r < n && arr[r] > arr[largest])
        largest = r;
    if (largest != i){
        swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}
void HeapSort(vector<int>&arr){
    int n=arr.size();
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i);
    for (int i=n-1; i>=0; i--){
        swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}
void InsertSort(vector<int>&arr) {
    int n=arr.size();
  int x,val,y;
  for(x = 1; x < n; x++) {
    val = arr[x];
    y = x - 1;
    while (y >= 0 && arr[y] > val) {
      arr[y + 1] = arr[y];
      y--;
    }
    arr[y + 1] = val;
  }
}
void quickSort(vector<int>&arr, int inicio, int final) {
    int i = inicio, f = final, tmp;
    if(final==-100){
        f=arr.size();
    }
  int x = arr[(inicio + final) / 2];
  do {
    while(arr[i] < x && f <= final) {
      i++;
    }
    while(x < arr[f] && f > inicio) {
      f--;
    }
    if(i <= f) {
      tmp = arr[i];
      arr[i] = arr[f];
      arr[f] = tmp;
      i++; f--;
    }
  } while(i <= f);
  if(inicio < f) {
    quickSort(arr,inicio,f);
  }
  if(i < final){
    quickSort(arr,i,final);
  }

}
void QuickSort(vector<int>&arr){
    quickSort(arr,0,arr.size());
}
double tiempo(void(*f)(vector<int>&),vector<int>&lst,double n){
    double tiempo;
    double promedio=0;
    for(int i=0;i<n;i++){
       // cout<<"I2: "<<i<<endl;
        vector<int> aux=lst;
        tiempo=clock();
        f(lst);
        promedio+=(clock()-tiempo);
    }

    return promedio/n;
    /*
    time_t t0,t1;
    time(&t0);
    f(lst);
    time(&t1);
    cout<<t1<<endl;
    return (double(t1-t0));*/
}
void generarDatos(int fi,int it,int numTrials,int listMax,string name){
    ofstream of;
    of.open(name.c_str(),ios::out);
    for (int i=it;i<=fi;i+=it){
        cout<<i<<endl;
        vector<int> v0,v1,v2,v3,v4,v5,v6;
        for(int j=0;j<i;j++){
            v0.push_back(rand()%listMax);
        }
        v1=v2=v3=v4=v5=v6=v0;
        of<<i<<";";
        of<<tiempo(QuickSort,v0,numTrials)<<";";
        of<<tiempo(BubbleSort,v1,numTrials)<<";";
        of<<tiempo(CountSort,v2,numTrials)<<";";
        of<<tiempo(HeapSort,v3,numTrials)<<";";
        of<<tiempo(InsertSort,v4,numTrials)<<";";
        of<<tiempo(MergeSort,v5,numTrials)<<";";
        of<<tiempo(SelectionSort,v6,numTrials)<<";"<<endl;
    }
    of.close();
}

int main(){
/*
    int n=13;
    int l[]={ 67, 49, 30, 25, 11, 48, 37, 66, 62, 28, 45, 33, 41 };
    vector<int> lista (l, l + sizeof(l) / sizeof(int) );
     // InsertSort(lista,n);
     // QuickSort(lista,0,n-1);
     // bubble(lista,n);
     // SelectionSort(lista,n);
     // heapSort(lista,n);
     // mergeSort(lista,0,n-1);
    //quickSort(lista,0,lista.size());*/

    generarDatos(10000,1000,20,1000,"cplus.csv");cout<<"termino"<<endl;

  //  for(int k=0;k<n;k++)cout<<lista[k]<<" ";cout<<endl;

   //graficar(InsertSort,10000,1000,5,1000,"InsertSort.csv");

}
