# Protocols for a Two-Tiered Trusted Computing Base - ProVerif Models

ProVerif models for the work

*Protocols for a Two-Tiered Trusted Computing Base.*  In: Atluri, V., Di Pietro, R., Jensen, C.D., Meng, W. (eds) Computer Security – ESORICS 2022. ESORICS 2022. Lecture Notes in Computer Science, vol 13556. Springer, Cham. https://doi.org/10.1007/978-3-031-17143-7_12

Presented in the European Symposium on Research in Computer Security (ESORICS), September 26-30, 2022, Copenhagen, Denmark.

## Authors
- José Moreira
- [Mark D. Ryan](https://www.cs.bham.ac.uk/~mdr/)
- [Flavio D. Garcia](https://www.cs.bham.ac.uk/~garciaf/)

## File summary
- `mtcb_protocol_1.epv`: Extended ProVerif model for Protocol 1 (A/B Udpate).
- `mtcb_protocol_234a.epv`: ProVerif model for Protocol 2 (Secure Boot), Protocol 3 (Attestation) and Protocol 4a (ETCB Recovery - Memory corruption detection).
- `mtcb_protocol_4b.epv`: ProVerif model for Protocol 4b (ETCB Recovery - Platform recovery).
- `macro_resolver.py`: Macro resolver - parses extended ProVerif code to ProVerif code.

## Requirements
- [Python 3](https://www.python.org/downloads/)
- [ProVerif v2.04](https://bblanche.gitlabpages.inria.fr/proverif/) or later

## Examples of usage
In the following example, we assume that Protocol 1 will execute 3 updates of the MTCB code.

```bash
python macro_resolver.py -i mtcb_protocol_1.epv -o mtcb_protocol_1.out.pv -r "i<3,j<3"

proverif -color mtcb_protocol_1.out.pv

proverif -color mtcb_protocol_234a.pv

proverif -color mtcb_protocol_4b.pv
```

*Note:* In order to obtain a full report in HTML format, we recommend to create a sub-directory
within the working directory, e.g., `mkdir <dir_name>`, and use the ProVerif
command line option `-html <dir_name>`.
See further command line options in the [ProVerif manual](https://bblanche.gitlabpages.inria.fr/proverif/manual.pdf).
