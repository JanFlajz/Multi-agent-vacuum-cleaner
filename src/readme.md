Toto je moje vypracování prvního domácího ukolu z NI-UMI. Jedná se o 1. příklad - vysavač, který má za úkol vysát všechna smítka v co nejkratším čase. Pozice všech smetí je dopředu známá, všechny vysavače začínají a končí na pozici 1,1.

Úlohu jsem řešil jako (m)TSP pomocí algoritmu optimalizace mravenčí kolonie (ACO algorithm), který je popsán v komentáři v příslušném pythonovém souboru. Pro vypočítání délky nejkratší trasy mezi 2 smetí jsem použil A*. 
Bludiště ve kterém vysavače hledají smetí 

Program má i GUI pomocí knihovny PysimpleGUI verze 4.60.5.0, ta je nainstalovaná ve virtuálním prostředí.

Spuštění:
pip -r install requirements.txt
python .\garbage_collectors.py [Počet agentů]

Doporučený počet agentů při mTSP je 3.