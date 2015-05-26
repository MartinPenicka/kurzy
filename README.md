# kurzy
Kalkulačka pro příkazový řádek pro převod cizích měn na koruny

Program parsuje data z webu ČNB. Data jsou po stáhnutí uložena lokálně do souboru /tmp/kurzy.db, při následujících dotazech již nestahuje dodatečná data. Data mají platnost do restartu počítače.

Příklad použití :

  - :~$kurz usd      -> vypíše cenu za jeden dolar
  - :~$kurz usd 25   -> vypíše cenu v korunách za 25 dolarů

Jako parametr přijímá program kód libovolné měny v databázi ČNB. 
