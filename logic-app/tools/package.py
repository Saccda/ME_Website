"""Create a portable source bundle, excluding credentials, private sources and local state."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root=Path(__file__).resolve().parents[1]
target=root.parent/'outputs'/'ME_RUPP_Logic_Studio_Source.zip'
target.parent.mkdir(exist_ok=True)
skip={'node_modules','.next','.venv','__pycache__','.pytest_cache','test-results','private','.git'}
with ZipFile(target,'w',ZIP_DEFLATED) as archive:
    for file in root.rglob('*'):
        relative=file.relative_to(root)
        if not file.is_file() or any(p in skip for p in relative.parts) or '.db' in file.name or file.name in {'.env','tsconfig.tsbuildinfo'}: continue
        archive.write(file,Path('logic-app')/relative)
    archive.write(root/'private'/'README.md','logic-app/private/README.md')
print(target)
