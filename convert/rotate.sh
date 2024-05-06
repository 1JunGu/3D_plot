convert test.png \( +clone -background black -shadow 80x3+5+5 \) +swap \
    -background none -layers merge +repage -rotate 10 test_rotate.png
