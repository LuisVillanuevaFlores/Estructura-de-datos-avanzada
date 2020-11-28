function M=mergeSort(A)
  size=length(A);
  if(size==1)
    M=A;
  else
    m=floor(size/2);
    L=mergeSort(A(1:m));
    R=mergeSort(A(m+1:size));  
    i=j=k=1;
    l=length(L);r=length(R);
    while(i<l+1 && j<r+1)
      if(L(i)<R(j))
        M(k)=L(i);
        i++;
      else
        M(k)=R(j);
        j++;
      endif
      k++;
    endwhile
    while(i<l+1)
      M(k)=L(i);
      i++;k++;
    endwhile
    while(j<r+1)
      M(k)=R(j);
      k++;j++;
    endwhile
  endif
endfunction

 

