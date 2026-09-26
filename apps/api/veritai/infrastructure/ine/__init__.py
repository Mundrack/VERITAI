"""Conector del INE (Instituto Nacional de Estadistica, Espana) via API Tempus.

Unico emisor de la Puerta 2 (DEC-024). Tres piezas:
    tempus.py      cliente HTTP con allowlist, timeout y tope de tamano
    extractor.py   del JSON crudo a series con el span literal de cada valor
    proveedor.py   implementa el puerto ProveedorEvidencia
"""
