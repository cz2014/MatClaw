# Biased molecular dynamics

Categories: Advanced molecular-dynamics sampling, Theory

*Biased molecular dynamics'* (MD) refers to advanced MD-simulation methods that introduce a *bias potential*. One of the most important purposes of using bias potentials is to enhance the sampling of phase space with low probability density (e.g., transition regions of chemical reactions). Depending on the type of sampling and in combination with the corresponding statistical methods one then has access to important thermodynamic quantities like, e.g., free energies. Biased molecular dynamics comes in very different flavors such as, e.g., umbrella sampling and umbrella integration, to name a few. For a comprehensive description (especially about umbrella sampling), we refer the interested user to Ref. written by D. Frenkel and B. Smit.

The probability density for a geometric parameter ξ of the system driven by a Hamiltonian

:   $$H(q,p) = T(p) + V(q), \;$$

with *T*(*p*), and *V*(*q*) being kinetic, and potential energies, respectively, can be written as

:   $$P(\xi\_i)=\frac{\int\delta\Big(\xi(q)-\xi\_i\Big) \exp\left\{-H(q,p)/k\_B\,T\right\} dq\,dp}{\int \exp\left\{-H(q,p)/k\_B\,T\right\}dq\,dp} =
    \langle\delta\Big(\xi(q)-\xi\_i\Big)\rangle\_{H}.$$

The term $\langle X \rangle\_H$ stands for a thermal average of quantity *X* evaluated for the system driven by the Hamiltonian *H*.

If the system is modified by adding a bias potential $\tilde{V}(\xi)$ acting on one or multiple selected internal coordinates of the system ξ=ξ(*q*), the Hamiltonian takes the form

:   $$\tilde{H}(q,p) = H(q,p) + \tilde{V}(\xi),$$

and the probability density of ξ in the biased ensemble is

:   $$\tilde{P}(\xi\_i)= \frac{\int \delta\Big(\xi(q)-\xi\_i\Big) \exp\left\{-\tilde{H}(q,p)/k\_B\,T\right\} dq\,dp}{\int \exp\left\{-\tilde{H}(q,p)/k\_B\,T\right\}dq\,dp} = \langle\delta\Big(\xi(q)-\xi\_i\Big)\rangle\_{\tilde{H}}.$$

It can be shown that the biased and unbiased averages are related via

:   $$P(\xi\_i)=\tilde{P}(\xi\_i) \frac{\exp\left\{\tilde{V}(\xi)/k\_B\,T\right\}}{\langle \exp\left\{\tilde{V}(\xi)/k\_B\,T\right\} \rangle\_{\tilde{H}}}.$$

More generally, an observable

:   $$\langle A \rangle\_{H} = \frac{\int A(q) \exp\left\{-H(q,p)/k\_B\,T\right\} dq\,dp}{\int \exp\left\{-H(q,p)/k\_B\,T\right\}dq\,dp}$$

can be expressed in terms of thermal averages within the biased ensemble as

:   $$\langle A \rangle\_{H} =\frac{\langle A(q) \,\exp\left\{\tilde{V}(\xi)/k\_B\,T\right\} \rangle\_{\tilde{H}}}{\langle \exp\left\{\tilde{V}(\xi)/k\_B\,T\right\} \rangle\_{\tilde{H}}}.$$

One of the most popular methods using bias potentials is umbrella sampling. This method uses a bias potential to enhance sampling of ξ in regions with low *P*(ξ*i*), e.g., transition regions of chemical reactions. The correct distributions are recovered afterward using the equation for $\langle A \rangle\_{H}$ above.

### How to

For a description of biased molecular dynamics see Biased molecular dynamics.

* For a biased molecular dynamics run with Andersen thermostat, one has to:

1. Set the standard MD-related tags: IBRION=0, TEBEG, POTIM, and NSW.
2. Choose thermostat:
   1. Set MDALGO=1 (or MDALGO=11 in VASP 5.x), and choose an appropriate setting for ANDERSEN\_PROB.
   2. Set MDALGO=2 (or MDALGO=21 in VASP 5.x), and choose an appropriate setting for SMASS.
3. In order to avoid updating of the bias potential, set HILLS\_BIN=NSW.
4. Define collective variables in the ICONST-file, and set the STATUS parameter for the collective variables to 5.
5. Define the bias potential in the PENALTYPOT file if necessary.

The values of all collective variables for each MD step are listed in the REPORT file. Check the lines after the string Metadynamics.

## References
