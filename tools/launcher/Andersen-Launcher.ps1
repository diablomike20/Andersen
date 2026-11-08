#requires -Version 5.1
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[Windows.Forms.Application]::EnableVisualStyles()
$Root=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if(-not(Test-Path (Join-Path $Root 'package.json'))){$Root=(Get-Location).Path}
if(-not(Test-Path (Join-Path $Root 'package.json'))){[Windows.Forms.MessageBox]::Show('Nem találom a package.json fájlt. A launchert a repository gyökeréből indítsd.','Andersen Launcher','OK','Error')|Out-Null;exit 1}
$C=@{Bg=[Drawing.Color]::FromArgb(8,13,26);Panel=[Drawing.Color]::FromArgb(15,27,44);Panel2=[Drawing.Color]::FromArgb(20,36,58);Gold=[Drawing.Color]::FromArgb(216,182,110);GoldLight=[Drawing.Color]::FromArgb(245,224,174);Text=[Drawing.Color]::FromArgb(248,243,230);Muted=[Drawing.Color]::FromArgb(166,180,199);Green=[Drawing.Color]::FromArgb(120,190,145);Red=[Drawing.Color]::FromArgb(220,125,115)}
$script:S=$null;$script:R=$null
function L($t,$x,$y,$w,$h,$z,$color,$font='Segoe UI'){$v=New-Object Windows.Forms.Label;$v.Text=$t;$v.Location=New-Object Drawing.Point($x,$y);$v.Size=New-Object Drawing.Size($w,$h);$v.ForeColor=$color;$v.BackColor=[Drawing.Color]::Transparent;$v.Font=New-Object Drawing.Font($font,$z);return $v}
function SetS($t,$ok=$true){if($script:S){$script:S.Text=$t;$script:S.ForeColor=if($ok){$C.Green}else{$C.Red}};[Windows.Forms.Application]::DoEvents()}
function CheckTools{$nv=$null;$pv=$null;$n=Get-Command node -ErrorAction SilentlyContinue;$p=Get-Command pnpm -ErrorAction SilentlyContinue;$cp=Get-Command corepack -ErrorAction SilentlyContinue;if($n){try{$nv=(& node --version 2>$null).Trim()}catch{}};if($p){try{$pv=(& pnpm --version 2>$null).Trim()}catch{}}elseif($cp){try{$pv=(& corepack pnpm --version 2>$null).Trim()}catch{}};$ok=$false;if($nv -match '^v?(\d+)\.(\d+)\.(\d+)'){$ok=([version]("$($Matches[1]).$($Matches[2]).$($Matches[3])") -ge [version]'22.19.0')};return [pscustomobject]@{NodeOK=$ok;NodeVersion=$nv;PnpmOK=($p -or $cp);PnpmVersion=$pv}}
function RunTask($task){$t=CheckTools;if(-not $t.NodeOK){SetS 'Node.js 22.19.0 vagy újabb szükséges.' $false;return};if(-not $t.PnpmOK){SetS 'A pnpm vagy Corepack nem található.' $false;return};if(-not(Test-Path (Join-Path $Root 'node_modules')) -and $task -ne 'install'){$a=[Windows.Forms.MessageBox]::Show('A függőségek hiányoznak. Elindítsam a pnpm install folyamatot?','Első indítás','YesNo','Question');if($a -eq 'Yes'){RunTask 'install'};return};$pm=if(Get-Command corepack -ErrorAction SilentlyContinue){'corepack pnpm'}else{'pnpm'};$cmd=switch($task){web{"$pm run dev"} desktop{"$pm run tauri:dev"} build{"$pm run build"} install{"$pm install"}};$safe=$Root.Replace("'","''");$line="Set-Location -LiteralPath '$safe'; $taskName=switch($task){web{'Webes fejlesztes'} desktop{'Asztali alkalmazas'} install{'Fuggosegek telepitese'} build{'Webes build'}}; title ANDERSEN - $taskName; $cmd";try{Start-Process powershell.exe -ArgumentList @('-NoExit','-ExecutionPolicy','Bypass','-Command',$line) -WorkingDirectory $Root;SetS "Indítás elindítva: $task"}catch{SetS "Indítási hiba: $($_.Exception.Message)" $false}}
function B($t,$x,$y,$w,$h,$primary=$false){$b=New-Object Windows.Forms.Button;$b.Text=$t;$b.Location=New-Object Drawing.Point($x,$y);$b.Size=New-Object Drawing.Size($w,$h);$b.FlatStyle='Flat';$b.FlatAppearance.BorderColor=$C.Gold;$b.FlatAppearance.BorderSize=1;$b.BackColor=if($primary){$C.Gold}else{$C.Panel2};$b.ForeColor=if($primary){$C.Bg}else{$C.GoldLight};$b.Font=New-Object Drawing.Font('Segoe UI Semibold',9,[Drawing.FontStyle]::Bold);$b.Cursor=[Windows.Forms.Cursors]::Hand;return $b}
$f=New-Object Windows.Forms.Form;$f.Text='ANDERSEN — Creative Writing Studio';$f.Size=New-Object Drawing.Size(820,650);$f.MinimumSize=$f.Size;$f.MaximumSize=$f.Size;$f.StartPosition='CenterScreen';$f.BackColor=$C.Bg
$p=New-Object Windows.Forms.Panel;$p.Location=New-Object Drawing.Point(12,12);$p.Size=New-Object Drawing.Size(780,586);$p.BackColor=$C.Bg;$p.BorderStyle='FixedSingle';$f.Controls.Add($p)
$a=L 'ALKOTÓI ÍRÓMŰHELY' 38 26 500 22 9 $C.Gold;$a.Font=New-Object Drawing.Font('Segoe UI Semibold',9,[Drawing.FontStyle]::Bold);$p.Controls.Add($a)
$a=L 'ANDERSEN' 34 52 520 70 35 $C.Text Georgia;$a.Font=New-Object Drawing.Font('Georgia',35,[Drawing.FontStyle]::Bold);$p.Controls.Add($a)
$p.Controls.Add((L 'A te világod. A te történeted. A te alkotásod.' 38 125 600 28 13 $C.GoldLight Georgia))
$r=New-Object Windows.Forms.Panel;$r.Location=New-Object Drawing.Point(38,165);$r.Size=New-Object Drawing.Size(700,1);$r.BackColor=$C.Gold;$p.Controls.Add($r)
$p.Controls.Add((L 'Adj teret a történetnek.' 38 184 650 30 17 $C.Text Georgia))
$p.Controls.Add((L 'Válaszd ki, hogyan szeretnéd megnyitni az alkotói műhelyt.' 38 218 680 24 9 $C.Muted))
$b=B 'WEBES FEJLESZTŐI MÓD' 38 266 330 58 $true;$b.Add_Click({RunTask 'web'});$p.Controls.Add($b)
$b=B 'ASZTALI ALKALMAZÁS' 388 266 350 58;$b.Add_Click({RunTask 'desktop'});$p.Controls.Add($b)
$b=B 'FÜGGŐSÉGEK TELEPÍTÉSE' 38 340 220 42;$b.Add_Click({RunTask 'install'});$p.Controls.Add($b)
$b=B 'WEBES BUILD KÉSZÍTÉSE' 273 340 220 42;$b.Add_Click({RunTask 'build'});$p.Controls.Add($b)
$b=B 'GITHUB-TÁRHÁZ MEGNYITÁSA' 508 340 230 42;$b.Add_Click({Start-Process 'https://github.com/diablomike20/Andersen'});$p.Controls.Add($b)
$r=New-Object Windows.Forms.Panel;$r.Location=New-Object Drawing.Point(38,410);$r.Size=New-Object Drawing.Size(700,1);$r.BackColor=[Drawing.Color]::FromArgb(65,216,182,110);$p.Controls.Add($r)
$a=L 'RENDSZERÁLLAPOT' 38 428 300 22 9 $C.Gold;$a.Font=New-Object Drawing.Font('Segoe UI Semibold',9,[Drawing.FontStyle]::Bold);$p.Controls.Add($a)
$script:R=L 'Ellenőrzés folyamatban…' 38 458 690 46 9 $C.Muted;$p.Controls.Add($script:R)
$script:S=L 'Készen áll.' 38 516 690 24 9 $C.Green;$p.Controls.Add($script:S)
$p.Controls.Add((L 'ÍRJ  ·  ALKOSS  ·  KÉPZELJ EL  ·  TEREMTS' 38 554 500 20 8 $C.Gold))
$a=L 'ANDERSEN INDÍTÓ / WINDOWS' 510 554 228 20 8 $C.Muted;$a.TextAlign='MiddleRight';$p.Controls.Add($a)
$f.Add_Shown({$t=CheckTools;$nv=if($t.NodeVersion){$t.NodeVersion}else{'nem található'};$pv=if($t.PnpmVersion){$t.PnpmVersion}else{'nem található'};$deps=if(Test-Path (Join-Path $Root 'node_modules')){'telepítve'}else{'nincs telepítve'};$script:R.Text="Node.js: $nv (elvárt >=22.19.0)"+[Environment]::NewLine+"pnpm: $pv (package.json: 12.13.0)    Függőségek: $deps";if($t.NodeOK -and $t.PnpmVersion -eq '12.13.0'){SetS 'A fejlesztői környezet készen áll.'}else{SetS 'Ellenőrizd a Node.js és pnpm verzióját.' $false}})
[void]$f.ShowDialog()
