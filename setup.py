from cx_Freeze import setup, Executable

setup(
    name="CompilaPasta",
    version="1.0",
    description="Minha Aplicação",
    executables=[
        Executable(
            "concatenador_pasta.py",
            target_name="concatena_pasta.exe",
            icon="icon.ico", # Substitua "seu_icone.ico" pelo caminho do seu arquivo de ícone
            base="Win32GUI"  # Para esconder o console em Windows
        )
    ]
)