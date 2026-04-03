# BSEFATBAND

Categories: Files, Output files, Bethe-Salpeter equations

The BSEFATBAND file contains the NBSEEIG number of eigenvectors of the BSE Hamiltonian.

The file has the following structure:

```
  rank of the BSE matrix                NBSEEIG
  1BSE eigenvalue    E_BSE      IP-eigenvalue:    E_IP
Kx Ky Kz E_v E_c Abs(X_BSE)/W_k NB_v NB_c Re(X_BSE)+ i*Im(X_BSE)   
...
  2BSE eigenvalue    E_BSE      IP-eigenvalue:    E_IP
Kx Ky Kz E_v E_c Abs(X_BSE)/W_k NB_v NB_c Re(X_BSE)+ i*Im(X_BSE)
...
   NBSEEIGBSE eigenvalue    E_BSE      IP-eigenvalue:    E_IP
Kx Ky Kz E_v E_c Abs(X_BSE)/W_k NB_v NB_c Re(X_BSE)+ i*Im(X_BSE)
```

where *E\_BSE* and *E\_IP* are the BSE and IP transition energies,
*KX KY KZ* the k-point coordinates,
*E\_v* and *E\_c* the eigenvalues of the valence and conduction band, respectively,
*X\_BSE* the component of the eigenvector,
*W\_k* the weight of the k point, and *NB\_v NB\_c* the valence and conduction orbital numbers.

## Related tags and articles

NBSEEIG, BSE calculations

---
