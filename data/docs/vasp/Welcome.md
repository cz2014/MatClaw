# Welcome

Let us take a tour through the resources that are available to you as a VASP user!

## Become a VASP user

The standard way to become a VASP user is that the head of your research group acquires a license and registers you as a user on the VASP Portal. At a high-performance-computing (HPC) center, you can then immediately get access to a VASP executable by stating your license number.

Alternatively, you can apply to participate in a workshop with hands-on experience. The VASP developers infrequently organize workshops that are announced in the news section of the VASP website. Additionally, there are many Universities offering courses where VASP is taught, as well as independent workshops by experienced VASP collaborators.

## Install VASP

If you have a more-or-less powerful compute infrastructure available to you, you can  install VASP by compiling it yourself. There are some calculations that can even run on a standard laptop, but we recommend a more powerful infrastructure to unlock the full potential of VASP. Download the source code of the latest release from the VASP Portal and follow the  installation guide on the  VASP Wiki. If you need help, post your question in the VASP Forum. There is a section addressing solely installation issues. To get a forum account, you need to be a registered VASP user.

Which hardware exactly fits your purpose depends on the kind of calculations you want to run. Furthermore, hardware development is a rapidly evolving field, so we cannot recommend specific hardware specifications, e.g., node size or a specific vendor, to you. Have a look at the [Toolchains |toolchains] we are frequently testing to ensure compatibility with the compilers that come with your desired hardware. Run some smaller test calculations to see how the calculations for your application scale and have a look at factors that influence the  performance of VASP. Particularly, consider what  parallelization options and  memory requirements apply.

## Basic usage

To get hands-on experience with the setup of a calculation, check out the tutorials based on Python notebooks. You will quickly learn how to create the input for VASP by creating the proper input files and setting the correct tags to select the algorithm or adjust parameters. Additionally, there are examples and tutorials on the VASP Wiki. A lecture on a quick start to ab-initio calculations is available on our YouTube channel.

## Navigate the VASP Wiki

The main page of the VASP Wiki shows featured topics that represents a rough book-like table of contents. It covers a range from introductory topics, (i.e., the theoretical background and calculation setup), over the central chapters (the electronic ground state, ionic degree of freedom, and excitations) up to some advanced considerations, (i.e., obtaining a local basis for the electronic state or optimizing performance).

Each category page provides an introduction to the topic. It links to tag and file documentation, further theory pages, and  how-to pages to describe common workflows. If the explanation is unclear or information is missing, visit the VASP Forum. The section Using VASP is dedicated to queries on the usage of VASP. The VASP developers are continuously improving the documentation, so this kind of feedback can help identify where we need to improve.

## Learn a new method

VASP has a broad spectrum of applications in different fields all the way from many-body perturbation theory to classical molecular dynamics. A quick start is usually to find a corresponding tutorial,  example or how-to page in the corresponding category. Also, study the theoretical background by watching video lectures on the VASP Channel, attending a workshop announced in the news section of the VASP website or a course at your University. To dive deeper, read theory pages in the corresponding category on the VASP Wiki and follow the related references.

## Analyze VASP output

The output files written by VASP depends on the kind of calculation you are running.
py4vasp is the most seamless tool to extract data from VASP calculations. It is a Python package developed by VASP developers and helps to get a quick look at data, as well as parse it to other common formats. Mind that it requires a VASP executable with HDF5 support. Apart from that, most output files are human-readable, and there are various third-party tools to visualize the results.

## Get help

First, consider whether your issue is amongst the known issues or frequently asked questions (FAQs).
Regarding installing or using VASP, the VASP developers try to answer your questions as swiftly as possible on the VASP Forum. We also greatly appreciate any bug report on the VASP Forum and created some space for user-to-user discussion. Please kindly understand that we offer support on a courtesy basis only and not as a contractual service. Thus, first carefully read the  VASP Wiki and perhaps consider if this is a research question that a literature search or your principal investigator (PI) could help with.

For any other issues, see how to contact the VASP team!
