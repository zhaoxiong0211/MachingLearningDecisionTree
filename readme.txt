If you want to test the accuracy of the validate set:
python p2_4_1.py -np 'btrain.csv' 'bvalidate.csv' -validate //(unpruned)
python p2_4_1.py -p 'btrain.csv' 'bvalidate.csv' -validate //(pruned)

If you want to predict test set:
python p2_4_1.py -np 'btrain.csv' 'btest.csv' -predict //(unpruned)
python p2_4_1.py -p 'btrain.csv' 'btest.csv' -predict //(pruned)