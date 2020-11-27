# KVUE_allergy_report
KVUE Austin area allergy report in your terminal. 

```console
$ ./KVUE_allergy_report.py 
 KVUE allergy report for 2020-11-27  
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ allergen ┃ severity               ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Grasses  │ 27 gr/m3 High          │
│ Molds    │ Medium with Alternaria │
│ Ragweed  │ 13 gr/m3 Medium        │
│ Trees    │ 13 gr/m3 Low           │
└──────────┴────────────────────────┘
```

Due to Google's botguard, tranditional screenscraping can not be used.  This script is a tad slow as it uses headless Firefox.

```console
$ time ./KVUE_allergy_report.py
...
real	0m5.925s
user	0m4.954s
sys	0m0.920s
```
