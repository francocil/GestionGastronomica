# setupTools.ps1
# Instalador incremental de herramientas globales, paquetes Python y dependencias npm
# Ejecutar desde tools: .\setupTools.ps1

$toolsFile = "requerimientosDeInstaladores.txt"
$toolsPath = Join-Path $PSScriptRoot $toolsFile

Write-Host "Leyendo herramientas desde el archivo..."

$tools = Get-Content $toolsPath

foreach ($tool in $tools) {

    if ($tool.StartsWith("#") -or $tool.Trim() -eq "") {
        continue
    }

    Write-Host ""
    Write-Host ("Verificando: " + $tool)

    # ---------------------------------------------------------
    # 1) Dependencias npm → formato: npm:paquete
    # ---------------------------------------------------------
    if ($tool.StartsWith("npm:")) {
        $pkg = $tool.Replace("npm:", "")
        Write-Host ("→ Instalando dependencia npm: " + $pkg)

        Set-Location ../frontend/web
        npm install $pkg
        Set-Location ../../tools

        continue
    }

    # ---------------------------------------------------------
    # 2) Comandos del sistema
    # ---------------------------------------------------------
    $exists = Get-Command $tool -ErrorAction SilentlyContinue

    if ($exists) {
        Write-Host ("OK " + $tool + " ya está instalado (comando del sistema).")
        continue
    }

    # ---------------------------------------------------------
    # 3) Paquetes Python
    # ---------------------------------------------------------
    $pipCheck = pip show $tool 2>$null

    if ($pipCheck) {
        Write-Host ("OK " + $tool + " ya está instalado (paquete Python).")
        continue
    }

    # ---------------------------------------------------------
    # 4) Instalación según tipo
    # ---------------------------------------------------------
    Write-Host ("FALLO " + $tool + " no está instalado. Instalando...")

    switch ($tool) {
        "python3" { winget install Python.Python.3 }
        "pip" { python -m ensurepip }
        "virtualenv" { pip install virtualenv }
        "nodejs" { winget install OpenJS.NodeJS }
        "npm" { winget install OpenJS.NodeJS }
        "git" { winget install Git.Git }

        default {
            Write-Host ("→ Instalando paquete Python: " + $tool)
            pip install $tool
        }
    }
}

Write-Host ""
Write-Host "Proceso completado."
