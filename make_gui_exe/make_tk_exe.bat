REM This is intended to be run with the .bat file directory as the working dir
if not exist make_tk_exe.bat (
    echo Missing make_tk_exe.bat in working directory
    pause
    exit
)
if not exist text2cc_tk.pyw (
    echo Missing text2cc_tk.pyw in working directory
    pause
    exit
)

REM Create and activate a conda env for packaging the .exe
call conda create -y --name make_text2cc_gui_exe python=3.9 --no-default-packages
call conda activate make_text2cc_gui_exe
REM List conda envs -- useful for debugging
call conda info --envs
REM Install dependencies
pip install bespon
pip install markdown
pip install pyinstaller
if exist ..\setup.py (
    if exist ..\text2cc (
        cd ..
        pip install .
        cd make_gui_exe
    ) else (
rem pip install text2qti to prevent retrieving the wrong package.  
        rem pip install text2qti
    )
) else (
  rem   pip install text2qti
)
REM Build .exe
FOR /F "tokens=* USEBACKQ" %%g IN (`python -c "import text2cc; print(text2cc.__version__)"`) do (SET "text2cc_VERSION=%%g")
del text2cc_tk_%text2cc_VERSION%.exe
REM Set windows exe version info
FOR /F "tokens=1,2,3 delims=." %%I in ("%text2cc_VERSION%") do (
    SET Maj=%%I
    SET Min=%%J
	 SET Par=%%K
	 SET Pri=0
 )

del version.txt
rem %Maj%, %Min%, %Par%,%Pri%
 (
    for %%I in (
        "VSVersionInfo("
  "ffi=FixedFileInfo("
     "filevers=(%Maj%, %Min%, %Par%,%Pri%),"
    "prodvers=(%Maj%, %Min%, %Par%,%Pri%),"
    "mask=0x3f,"
    "flags=0x0,"
    "OS=0x40004,"
    "fileType=0x1,"
    "subtype=0x0,"
    "date=(0, 0)"
    "),"
  "kids=["
    "StringFileInfo("
      "["
      "StringTable("
        "u'040904B0',"
        "[StringStruct(u'CompanyName', u'Text2CC'),"
        "StringStruct(u'FileDescription', u'Text2CC'),"
        "StringStruct(u'FileVersion', u'%Maj%.%Min%.%Par%.%Pri%'),"
        "StringStruct(u'InternalName', u'Text2CC'),"
        
        "StringStruct(u'OriginalFilename', u'Text2CC.Exe'),"
        "StringStruct(u'ProductName', u'Text2CC'),"
        "StringStruct(u'ProductVersion', u'%Maj%.%Min%.%Par%.%Pri%')])"
      "])," 
    "VarFileInfo([VarStruct(u'Translation', [1033, 1200])])"
  "]"
")"
    ) do echo %%~I >> version.txt
)



pyinstaller -F --name text2cc_tk_%text2cc_VERSION% text2cc_tk.pyw --version-file version.txt

REM Deactivate and delete conda env
call conda deactivate
call conda remove -y --name make_text2cc_gui_exe --all
REM List conda envs -- useful for debugging
call conda info --envs
REM Cleanup
move dist\text2cc_tk_%text2cc_VERSION%.exe text2cc_tk_%text2cc_VERSION%.exe
rd /s /q "__pycache__"
rd /s /q "build"
rd /s /q "dist"
del *.spec
del version.txt
pause