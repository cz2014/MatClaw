# MAXMEM

Categories: INCAR tag, Many-body perturbation theory, GW, Low-scaling GW and RPA, Memory

MAXMEM = [integer]  
 Default: **MAXMEM** = 2800 (VASP.5.4.4. and older), automatically set as of VASP.6

Description: MAXMEM specifies the maximum memory one MPI rank will attempt to allocate (in MByte).
Since, the default varies somewhat between VASP versions, it is safer to set this
flag manually. Currently the flag is only inspected in few selected routines, such as
the GW or RPA routines that can use excessive amounts of memory. It is recommended to set
MAXMEM to the available memory per core minus 200 Mbyte. For instance, if one node is equipped
with 12 Gbyte, and 6 MPI ranks share this memory, the recommended setting is 12\*1024/6-200 = 1848.

---

As of VASP.6 the default value of MAXMEM is set to 90 percent of the available memory per MPI rank. If more than one compute node is used, the minimum of all nodes is used. The available memory in RAM is estimated by searching the file "/proc/meminfo" for the entry "MemAvailable:". Note that "/proc/meminfo" is present on any Linux system and stored in RAM. In case that the file cannot be found, MAXMEM is set to 2800.

---

## Related tags and articles

GW calculations, ACFDT calculations,
NTAUPAR

Examples that use this tag

---
