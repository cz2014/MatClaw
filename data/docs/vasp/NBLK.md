# NBLK

Categories: INCAR tag, Performance

NBLK = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **NBLK** | = -1 | VASP.4.6 |
|  | = 256 | in VASP.5.2, if dfast |

Description: NBLK determines the blocking factor in many BLAS level 3 routines.

---

In some cases, VASP has to perform a unitary transformation of the current orbitals. This is done using a work array CBLOCK and the following FORTRAN code:

```
      DO 100 IBLOCK=0,NPL-1,NBLK
         ILEN=MIN(NBLK,NPL-IBLOCK)
         DO 200 N1=1,N
            DO 200 M=1,ILEN
            CBLOCK(M,N1)=C(M+IBLOCK,N1)
            C(M+IBLOCK,N1)=0
  200    CONTINUE
C        C(IBLOCK+I,N)=SUM_(J,K) CH(I,K) CBLOCK(K,N)
         CALL ZGEMM ('N', 'N', ILEN, N, N, (1.,0.), CBLOCK, NBLK, CH, N,
              &   (1.,0.), C(IBLOCK+1,1), NDIM)
  100 CONTINUE
```

ZGEMM is the matrix $\times$ matrix multiplication command of the BLAS package. The task performed by this call is indicated by the comment line written above the ZGEMM call. Generally NBLK=16 or 32 is large enough for super-scalar machines. A large value might be necessary on vector machines for optimal performance (NBLK=128).

Examples that use this tag

---
