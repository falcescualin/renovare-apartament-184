$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$archiveRoot = Join-Path $projectRoot '_arhiva\2026-10-06_organizare'
$relativeFiles = @(
 'montaj_electric_R04.FCStd', 'montaj_electric_R06.FCStd',
 'montaj_electric_R07.FCStd', 'montaj_electric_R07_Vizibil.FCStd',
 'montaj_electric_R08_3D.FCStd',
 'output\pdf\Apartament_184_Montaj_electric_R05.pdf',
 'output\pdf\Apartament_184_Montaj_electric_R06.pdf',
 'output\pdf\Apartament_184_Montaj_electric_R07.pdf',
 'output\pdf\Apartament_184_Montaj_comparatie_R08.pdf',
 'output\pdf\Apartament_184_Plan_electric_R03.pdf',
 'output\pdf\Apartament_184_Plan_electric_R04.pdf',
 'output\pdf\Apartament_184_Registru_electric_R03.csv',
 'output\pdf\Apartament_184_Registru_electric_R04.csv',
 'output\pdf\Apartament_184_Prinderi_R08.csv',
 'output\pdf\Apartament_184_Registru_trasee_R08.csv',
 'output\pdf\Apartament_184_Segmente_R08.csv',
 'output\pdf\Apartament_184_Tuburi_R08.csv',
 'output\pdf\Apartament_184_Verificare_trasee_R05.csv',
 'output\pdf\Apartament_184_Verificare_trasee_R06.csv',
 'output\pdf\Apartament_184_Verificare_trasee_R07.csv'
)
$relativeFiles += Get-ChildItem -LiteralPath $projectRoot -File | Where-Object { $_.Extension -in '.FCBak','.blend1' } | ForEach-Object { $_.Name }
$records = @()
foreach ($relativeFile in $relativeFiles) {
 $sourceFile = [IO.Path]::GetFullPath((Join-Path $projectRoot $relativeFile))
 $targetFile = [IO.Path]::GetFullPath((Join-Path $archiveRoot $relativeFile))
 if (-not $sourceFile.StartsWith($projectRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Source outside project' }
 if (-not $targetFile.StartsWith($archiveRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Target outside archive' }
 if (-not (Test-Path -LiteralPath $sourceFile)) { continue }
 if (Test-Path -LiteralPath $targetFile) { throw "Destination already exists: $relativeFile" }
 $hash = (Get-FileHash -LiteralPath $sourceFile -Algorithm SHA256).Hash
 New-Item -ItemType Directory -Path (Split-Path -Parent $targetFile) -Force | Out-Null
 Move-Item -LiteralPath $sourceFile -Destination $targetFile
 if ((Get-FileHash -LiteralPath $targetFile -Algorithm SHA256).Hash -ne $hash) { throw 'Hash mismatch' }
 $records += [PSCustomObject]@{ Original=$relativeFile; Archive=$targetFile.Substring($projectRoot.Length+1); SHA256=$hash }
}
$records | Export-Csv -LiteralPath (Join-Path $archiveRoot 'MANIFEST_mutari.csv') -NoTypeInformation -Encoding UTF8
Write-Output "Archived and verified: $($records.Count) files."
