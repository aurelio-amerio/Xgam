```bash
python Xgam/bin/mkdataselection.py -c Xgam/config/config_dataselection_5w.py | tee /archive/home/Xgam/fermi_data/logs/5w_terminal_output.txt

python Xgam/bin/mkdataselection.py -c Xgam/config/config_dataselection_6y.py
python Xgam/bin/mkdataselection.py -c Xgam/config/config_dataselection_10y.py

python Xgam/bin/mkmask.py -c Xgam/config/config_mask.py --srcmask True --gpmask flat --extsrcmask True

python Xgam/bin/mkmask.py -c Xgam/config/config_mask_n64_simple.py --srcmask True --gpmask flat --extsrcmask True

python Xgam/bin/mkmask.py -c Xgam/config/config_mask_n64.py --srcweightedmask2 True --gpmask flat --extsrcmask True
```