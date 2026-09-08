# =============================================================================
# Genera el archivo .env local a partir de .env.example, con contrasenas
# aleatorias. El .env resultante esta en .gitignore y no se sube nunca.
#
#     .\scripts\init-env.ps1           crea .env si no existe
#     .\scripts\init-env.ps1 -Force    lo regenera (invalida los datos ya
#                                      guardados en el volumen de Postgres)
# =============================================================================
[CmdletBinding()]
param(
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

$Raiz      = Split-Path -Parent $PSScriptRoot
$Plantilla = Join-Path $Raiz '.env.example'
$Destino   = Join-Path $Raiz '.env'

if (-not (Test-Path $Plantilla)) {
    Write-Error 'No se encuentra .env.example'
}

if ((Test-Path $Destino) -and (-not $Force)) {
    Write-Host 'El archivo .env ya existe. No se toca.'
    Write-Host 'Para regenerarlo:  .\scripts\init-env.ps1 -Force'
    Write-Host 'AVISO: cambiar la contrasena de Postgres despues de crear el volumen'
    Write-Host '       obliga a "docker compose down -v", que BORRA los datos.'
    exit 0
}

function New-ContrasenaAleatoria {
    # Alfanumerica: la contrasena viaja dentro de una URL de conexion y no debe
    # contener caracteres que haya que escapar.
    $bytes = New-Object byte[] 64
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try { $rng.GetBytes($bytes) } finally { $rng.Dispose() }
    $texto = ([Convert]::ToBase64String($bytes)) -replace '[^A-Za-z0-9]', ''
    return $texto.Substring(0, 32)
}

$PassMigrator = New-ContrasenaAleatoria
$PassApp      = New-ContrasenaAleatoria
$Marcador     = 'GENERAR_CON_init-env'

$lineas = Get-Content -Path $Plantilla -Encoding UTF8 | ForEach-Object {
    $linea = $_
    if ($linea.StartsWith('POSTGRES_PASSWORD=')) {
        "POSTGRES_PASSWORD=$PassMigrator"
    }
    elseif ($linea.StartsWith('VERITAI_APP_DB_PASSWORD=')) {
        "VERITAI_APP_DB_PASSWORD=$PassApp"
    }
    elseif ($linea.StartsWith('DATABASE_URL_MIGRATOR=')) {
        $linea.Replace($Marcador, $PassMigrator)
    }
    elseif ($linea.StartsWith('DATABASE_URL=')) {
        $linea.Replace($Marcador, $PassApp)
    }
    else {
        $linea
    }
}

# Se escribe con LF y sin BOM a proposito. Docker Compose se lleva el \r final
# dentro del valor, asi que un .env con CRLF produce una contrasena invalida
# y un error de autenticacion que no dice cual es la causa.
$contenido = ($lineas -join "`n") + "`n"
$utf8SinBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($Destino, $contenido, $utf8SinBom)

Write-Host "Archivo .env creado en $Destino"
Write-Host 'Contrasenas generadas al azar. No las copies a ningun otro sitio.'
Write-Host ''
Write-Host 'Siguiente paso:  docker compose up -d'
