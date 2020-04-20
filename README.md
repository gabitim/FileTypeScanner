# FileTypeScanner

Dupa urmatoarele criterii, aplicatia scaneaza continutul binar al unui file si 
determina tipul de fisier

-text ASCII/UTF8 (frecvențe mari pentru caractere în limitele {9,10,13,32...127} și
     frecvențe foarte mici pentru caractere în limitele {0...8,11,12,14,15...31, 128...255})
-text UNICODE/UTF16 (caracterul 0 apare în cel puțin 30% din tot textul)
-binar (frecvențele sunt distribuite oarecum uniform pe tot domeniul {0...255})
-BMP  
-XML  
