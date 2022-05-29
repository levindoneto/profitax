# profitax
Cálculo de Lucros B3.

### Notas
- Considera ações fracionárias e lotes como a mesma ação (e.g.: ALUP3 == ALUP3F).

### Como usar
O arquivo acoes_ano_atual.csv é o que pode ser exportado no portal da B3. Já o acoes_stock.csv deve conter as informações declaradas como bens e direitos (code 31), vide exemplo na pasta de [exemplos](/exemplos).

```
python main.py acoes_ano_atual.csv acoes_stock.csv
```
